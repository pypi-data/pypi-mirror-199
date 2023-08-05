# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Common helper class for reading AzureML MLTable"""

import json
import logging
import os
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Union, cast

import azureml.dataprep as dprep
from azureml.core import Dataset as AmlDataset
from azureml.core import Run, Workspace
from azureml.data.abstract_dataset import AbstractDataset
from azureml.dataprep.api.engineapi.typedefinitions import FieldType
from azureml.dataprep.api.functions import get_portable_path
from azureml.exceptions import UserErrorException

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


@dataclass
class ImageDataFrameConstants:
    """
    A class to represent constants for image dataframe
    """

    LABEL_COLUMN_PROPERTY = "_Label_Column:Label_"
    DEFAULT_LABEL_COLUMN_NAME = "label"
    COLUMN_PROPERTY = "Column"
    IMAGE_COLUMN_PROPERTY = "_Image_Column:Image_"
    PORTABLE_PATH_COLUMN_NAME = "PortablePath"
    DEFAULT_IMAGE_COLUMN_NAME = "image_url"


@dataclass
class WorkspaceConstants:
    """
    Class representing the workspace related constants
    """

    WORKSPACE_CONFIG_FILENAME = "config.json"
    SUBSCRIPTION_ID = "subscription_id"
    RESOURCE_GROUP = "resource_group"
    WORKSPACE_NAME = "workspace_name"


def remove_leading_backslash(image_path: Union[str, Path]) -> str:
    """Utility method to remove the leading backslash from the image path
    :param image_path: Path of the image
    :type image_path: string

    :return: image path without leading backslash
    :rtype: str
    """
    if not image_path:
        return image_path
    if type(image_path) != str:
        image_path = str(image_path)
    return image_path if image_path[0] != "/" else image_path[1:]


class WorkspaceManager:
    """
    Class to serialize and deserilize the workspace object
    """

    @staticmethod
    def save(path: Path):
        """Serializes the workspace object on the provided path as a json file
        :param path: Path where the workspace object is serialized.
        :type path: pathlib.Path
        """
        try:
            ws = Run.get_context().experiment.workspace
        except Exception as e:
            logger.info(f"Failed to get workspace from run {e}")
            logger.info("Loading from_config")
            ws = Workspace.from_config()
        download_path = path / WorkspaceConstants.WORKSPACE_CONFIG_FILENAME
        workspace_config = {
            WorkspaceConstants.SUBSCRIPTION_ID: ws.subscription_id,
            WorkspaceConstants.RESOURCE_GROUP: ws.resource_group,
            WorkspaceConstants.WORKSPACE_NAME: ws.name,
        }
        with open(download_path, "w") as file:
            json.dump(workspace_config, file)

    @staticmethod
    def load(path: str) -> Workspace:
        """De-serializes the workspace object from the config present on the
         provided path
        :param path: Path to the config.json file or the directory containing
        the config.json file.
        :type path: str

        :return: The workspace object
        :rtype: azureml.core.Workspace
        """
        ws = Workspace.from_config(path=path)
        return ws


class DownloadManager:
    """A helper class that reads MLTable, download images and prepares the dataframe"""

    def __init__(
        self,
        mltable_path: str,
        ignore_data_errors: bool = False,
        image_column_name: str = ImageDataFrameConstants.DEFAULT_IMAGE_COLUMN_NAME,
        download_files: bool = True,
        ws: Workspace = None,
    ):

        """Constructor - This reads the MLTable and downloads the images that it contains.

        :param mltable_path: azureml MLTable path
        :type mltable_path: str
        :param ignore_data_errors: Setting this ignores and files in the dataset that fail to download.
        :type ignore_data_errors: bool
        :param image_column_name: The column name for the image file.
        :type image_column_name: str
        :param download_files: Flag to download files or not.
        :type download_files: bool
        :param workspace: Workspace the dataset is registered in. In case ws is None,
        it will be fetched from the Run object.
        :type workspace: azureml.core.Workspace
        """
        self._dataset = DownloadManager._get_dataset_from_mltable(mltable_path, ws)

        self._data_dir = DownloadManager._get_data_dir()

        self._image_column_name = DownloadManager._get_image_column_name(self._dataset, image_column_name)
        self._label_column_name = DownloadManager._get_label_column_name(
            self._dataset, ImageDataFrameConstants.DEFAULT_LABEL_COLUMN_NAME
        )

        if download_files:
            DownloadManager._download_image_files(self._dataset, self._image_column_name)

        dflow = self._dataset._dataflow.add_column(
            get_portable_path(dprep.col(self._image_column_name)),
            ImageDataFrameConstants.PORTABLE_PATH_COLUMN_NAME,
            self._image_column_name,
        )
        self._images_df = dflow.to_pandas_dataframe(extended_types=True)

        # drop rows for which images are not downloaded
        if download_files and ignore_data_errors:
            missing_file_indices = []
            for index in self._images_df.index:
                full_path = self._get_image_full_path(index)
                if not os.path.exists(full_path):
                    missing_file_indices.append(index)
                    msg = "File not found. Since ignore_data_errors is True, this file will be ignored."
                    logger.warning(msg)
            self._images_df.drop(missing_file_indices, inplace=True)
            self._images_df.reset_index(inplace=True, drop=True)

        # Put absolute path in the image_url column
        self._images_df[self._image_column_name] = self._images_df[
            ImageDataFrameConstants.PORTABLE_PATH_COLUMN_NAME
        ].apply(lambda row: os.path.join(self._data_dir, remove_leading_backslash(row)))

    @staticmethod
    def _get_dataset_from_mltable(mltable_path: str, ws: Workspace = None) -> AbstractDataset:
        """Get dataset from mltable.

        :param mltable_path: MLTable containing dataset URI
        :type mltable_path: str
        :param workspace: workspace the dataset is registered in
        :type workspace: azureml.core.Workspace
        :return: The dataset corresponding to given label.
        :rtype: AbstractDataset
        """

        dataset = None
        if mltable_path is None:
            raise UserErrorException(f"Mltable path is not provided, is {mltable_path}.")
        else:
            try:
                dataset = DownloadManager._load_abstract_dataset(mltable_path, ws)
            except (UserErrorException, ValueError) as e:
                msg = f"MLTable input is invalid. {e}"
                raise UserErrorException(msg)
            except Exception as e:
                msg = f"Error in loading MLTable. {e}"
                raise Exception(msg)

        return dataset

    @staticmethod
    def _load_abstract_dataset(mltable_path: str, ws: Workspace = None) -> AbstractDataset:
        """Get abstract dataset  from mltable.

        :param mltable_path: MLTable containing dataset URI
        :type mltable_path: str
        :param ws: Workspace the dataset is registered in.
        In case ws is None, it will be fetched from the Run object.
        :type workspace: azureml.core.Workspace
        :return: The dataset corresponding to given label.
        :rtype: AbstractDataset
        """
        if ws is None:
            try:
                ws = Run.get_context().experiment.workspace
            except Exception as e:
                logger.info(f"Failed to get workspace from run {e}")
                logger.info("Loading from_config")
                ws = Workspace.from_config()

        return AbstractDataset._load(mltable_path, ws)

    def _get_image_full_path(self, index: int) -> str:
        """Return the full local path for an image.

        :param index: index
        :type index: int
        :return: Full path for the local image file
        :rtype: str
        """
        rel_path = self._images_df[self._image_column_name].iloc[index]
        abs_path = os.path.join(self._data_dir, str(rel_path))
        return abs_path

    @staticmethod
    def _get_data_dir() -> str:
        """Get the data directory to download the image files to.

        :return: Data directory path
        :type: str
        """
        return tempfile.gettempdir()

    @staticmethod
    def _get_column_name(ds: AmlDataset, parent_column_property: str, default_value: str) -> str:
        """Get the column name by inspecting AmlDataset properties.
        Return default_column_name if not found in properties.

        :param ds: Aml Dataset object
        :type ds: TabularDataset
        :param parent_column_property: parent column property of the AmlDataset
        :type parent_column_property: str
        :param default_value: default value to return
        :type default_value: str
        :return: column name
        :rtype: str
        """
        if parent_column_property not in ds._properties:
            return default_value
        else:
            image_property = ds._properties[parent_column_property]
            if ImageDataFrameConstants.COLUMN_PROPERTY in image_property:
                return cast(str, image_property[ImageDataFrameConstants.COLUMN_PROPERTY])
            lower_column_property = ImageDataFrameConstants.COLUMN_PROPERTY.lower()
            if lower_column_property in image_property:
                return cast(str, image_property[lower_column_property])

    @staticmethod
    def _get_image_column_name(ds: AmlDataset, default_image_column_name: str) -> str:
        """Get the image column name by inspecting AmlDataset properties.
        Return default_image_column_name if not found in properties.

        :param ds: Aml Dataset object
        :type ds: TabularDataset
        :param default_image_column_name: default value to return
        :type default_image_column_name: str
        :return: Image column name
        :rtype: str
        """
        return DownloadManager._get_column_name(
            ds, ImageDataFrameConstants.IMAGE_COLUMN_PROPERTY, default_image_column_name
        )

    @staticmethod
    def _get_label_column_name(ds: AmlDataset, default_label_column_name: str) -> str:
        """Get the label column name by inspecting AmlDataset properties.
        Return default_label_column_name if not found in properties.

        :param ds: Aml Dataset object
        :type ds: TabularDataset
        :param default_label_column_name: default value to return
        :type default_label_column_name: str
        :return: Label column name
        :rtype: str
        """
        return DownloadManager._get_column_name(
            ds, ImageDataFrameConstants.LABEL_COLUMN_PROPERTY, default_label_column_name
        )

    @staticmethod
    def _download_image_files(ds, image_column_name: str) -> None:
        """Helper method to download dataset files.

        :param ds: Aml Dataset object
        :type ds: TabularDataset
        :param image_column_name: The column name for the image file.
        :type image_column_name: str
        """
        DownloadManager._validate_image_column(ds, image_column_name)
        logger.info("Start downloading image files")
        start_time = time.perf_counter()
        data_dir = DownloadManager._get_data_dir()
        logger.info(f"downloading images at path {data_dir}")
        try:
            ds.download(
                stream_column=image_column_name,
                target_path=data_dir,
                ignore_not_found=True,
                overwrite=True,
            )
        except Exception as e:
            logger.error(
                "Could not download dataset files. " f"Please check the logs for more details. Error Code: {e}"
            )
            raise Exception(e)

        logger.info(f"Downloading image files took {time.perf_counter() - start_time:.2f} seconds")

    @staticmethod
    def _validate_image_column(ds: AmlDataset, image_column_name: str) -> None:
        """Helper method to validate if image column is present in dataset, and it's type is STREAM.

        :param ds: Aml Dataset object
        :type ds: TabularDataset
        :param image_column_name: The column name for the image file.
        :type image_column_name: str
        """
        dtypes = ds._dataflow.dtypes
        if image_column_name not in dtypes:
            raise UserErrorException(f"Image URL column '{image_column_name}' is not present in the dataset.")

        image_column_dtype = dtypes.get(image_column_name)
        if image_column_dtype != FieldType.STREAM:
            raise UserErrorException(
                f"The data type of image URL column '{image_column_name}' is {image_column_dtype.name}, "
                f"but it should be {FieldType.STREAM.name}."
            )
