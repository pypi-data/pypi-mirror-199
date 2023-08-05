from typing import Any, Dict, List, Optional, Union, Tuple, cast

from .dataset_client import DatasetClient
from .base_labels import (
    _BaseCrop,
    _BaseSingleCrop,
    _BaseCropSet,
    _Bbox2D,
    _Classification2D,
    _Classification3D,
    _Cuboid3D,
    _Keypoint2D,
    _LineSegment2D,
    _PolygonList2D,
    _Semseg2D,
    _InstanceSeg2D,
    _TextToken,
)

from .util import (
    KEYPOINT_KEYS,
    POLYGON_VERTICES_KEYS,
    ResizeMode,
    InstanceSegInstance as InstanceSegInstance,
)


class _Label:
    pass


# TODO: figure out how to get nice typechecking and typehinting without having to list out these args every time
class Bbox2DLabel(_Label, _Bbox2D):
    """Create a label for a 2D bounding box.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this label
        top: The top of the box in pixels
        left: The left of the box in pixels
        width: The width of the box in pixels
        height: The height of the box in pixels
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        top: Union[int, float],
        left: Union[int, float],
        width: Union[int, float],
        height: Union[int, float],
        sensor_id: str = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        super(Bbox2DLabel, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            top=top,
            left=left,
            width=width,
            height=height,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class LineSegment2DLabel(_Label, _LineSegment2D):
    """Create a 2D line segment label.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this label
        x1: The x-coord of the first vertex in pixels
        y1: The x-coord of the first vertex in pixels
        x2: The x-coord of the first vertex in pixels
        y2: The x-coord of the first vertex in pixels
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        x1: Union[int, float],
        y1: Union[int, float],
        x2: Union[int, float],
        y2: Union[int, float],
        sensor_id: str = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        super(LineSegment2DLabel, self).__init__(
            "ADD",
            id,
            classification=classification,
            sensor_id=sensor_id,
            x1=x1,
            x2=x2,
            y1=y1,
            y2=y2,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class Keypoint2DLabel(_Label, _Keypoint2D):
    """Create a label for a 2D Keypoint.

    A keypoint is a dictionary of the form:
        'x': x-coordinate in pixels
        'y': y-coordinate in pixels
        'name': string name of the keypoint

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this label
        keypoints: The keypoints of this detection
        top: The top of the bounding box in pixels. Defaults to None.
        left: The left of the bounding box in pixels. Defaults to None.
        width: The width of the bounding box in pixels. Defaults to None.
        height: The height of the bounding box in pixels. Defaults to None.
        polygons: The polygon geometry. Defaults to None.
        center: The center point of the polygon instance. Defaults to None.
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        keypoints: List[Dict[KEYPOINT_KEYS, Union[int, float, str]]],
        top: Optional[Union[int, float]] = None,
        left: Optional[Union[int, float]] = None,
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        polygons: Optional[
            List[Dict[POLYGON_VERTICES_KEYS, List[Tuple[Union[int, float]]]]]
        ] = None,
        center: Optional[List[Union[int, float]]] = None,
        sensor_id: str = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ) -> None:
        super(Keypoint2DLabel, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            keypoints=keypoints,
            top=top,
            left=left,
            width=width,
            height=height,
            polygons=polygons,
            iscrowd=iscrowd,
            center=center,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class PolygonList2DLabel(_Label, _PolygonList2D):
    """Create a label for a 2D polygon list for instance segmentation

    Polygons are dictionaries of the form:
        'vertices': List of (x, y) vertices (e.g. [[x1,y1], [x2,y2], ...])
            The polygon does not need to be closed with (x1, y1).
            As an example, a bounding box in polygon representation would look like:

            .. code-block::

                {
                    'vertices': [
                        [left, top],
                        [left + width, top],
                        [left + width, top + height],
                        [left, top + height]
                    ]
                }

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this label
        polygons: The polygon geometry.
        center: The center point of the polygon instance. Defaults to None.
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        polygons: List[Dict[POLYGON_VERTICES_KEYS, List[Tuple[Union[int, float]]]]],
        center: Optional[List[Union[int, float]]] = None,
        sensor_id: str = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ) -> None:
        super(PolygonList2DLabel, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            polygons=polygons,
            center=center,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class Semseg2DLabel(_Label, _Semseg2D):
    """
    Add a mask for 2D semseg.

    Args:
        id: Id which is unique across datasets and inferences.
        mask_url: URL to the pixel mask png.
        resize_mode (Optional[ResizeMode]): (optional) If the mask is a different size from the base image, define how to display it. "fill" will stretch the mask to fit the base image dimensions. None will do nothing.
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
    """

    def __init__(
        self,
        *,
        id: str,
        mask_url: str,
        resize_mode: Optional[ResizeMode] = None,
        sensor_id: str = None,
    ):

        super(Semseg2DLabel, self).__init__(
            "ADD",
            id=id,
            sensor_id=sensor_id,
            mask_url=mask_url,
            resize_mode=resize_mode,
        )


class InstanceSeg2DLabel(_Label, _InstanceSeg2D):
    """Create an 2D instance segmentation label.

    Args:
        id: Id which is unique across datasets and inferences.
        mask_url: URL to the pixel mask png.
        instances: A list of instances present in the mask
        resize_mode (Optional[ResizeMode]): (optional) If the mask is a different size from the base image, define how to display it. "fill" will stretch the mask to fit the base image dimensions. None will do nothing.
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
    """

    def __init__(
        self,
        *,
        id: str,
        mask_url: str,
        instances: List[InstanceSegInstance],
        resize_mode: Optional[ResizeMode] = None,
        sensor_id: str = None,
    ):
        for instance in instances:
            if not isinstance(instance, InstanceSegInstance):
                raise Exception(
                    "Can only add InstanceSegInstance instances to a new InstanceSeg2D Label"
                )

        super(InstanceSeg2DLabel, self).__init__(
            "ADD",
            id=id,
            sensor_id=sensor_id,
            mask_url=mask_url,
            instances=instances,
            resize_mode=resize_mode,
        )


class Classification2DLabel(_Label, _Classification2D):
    """Create a 2D classification label.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification string
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
        secondary_labels: (optional) Dictionary of secondary labels
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        sensor_id: str = None,
        secondary_labels: Optional[Dict[str, Any]] = None,
        user_attrs: Optional[Dict[str, Any]] = {},
    ):
        super(Classification2DLabel, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            secondary_labels=secondary_labels,
            user_attrs=user_attrs,
        )


class Classification3DLabel(_Label, _Classification3D):
    """Create a 3D classification label.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification string
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        sensor_id: str = None,
        user_attrs: Optional[Dict[str, Any]] = {},
    ):
        super(Classification3DLabel, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            user_attrs=user_attrs,
        )


class Cuboid3DLabel(_Label, _Cuboid3D):
    """Add a label for a 3D cuboid.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this label
        position: The position of the center of the cuboid
        dimensions: The dimensions of the cuboid
        rotation: The local rotation of the cuboid, represented as an xyzw quaternion.
        coordinate_frame_id: (optional) The id of the coordinate frame to attach this label to (if not set, we will try to infer this from the frame's coordinate frames)
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        position: List[float],
        dimensions: List[float],
        rotation: List[float],
        coordinate_frame_id: str = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = {},
        embedding: Optional[List[float]] = None,
    ):
        super(Cuboid3DLabel, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            coordinate_frame_id=coordinate_frame_id,
            position=position,
            dimensions=dimensions,
            rotation=rotation,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class TextTokenLabel(_Label, _TextToken):
    """Create a text token label.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this label
        index: The index of this token in the text
        token: The text content of this token
        visible: Is this a visible token in the text
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        index: int,
        token: str,
        visible: bool,
        sensor_id: str = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = {},
        embedding: Optional[List[float]] = None,
    ):
        super(TextTokenLabel, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            index=index,
            token=token,
            visible=visible,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class _LabeledSet(_BaseCropSet):
    """The internal class for organizing labels attached to a frame

    :meta private:
    """

    def __init__(self, frame_id: str, dataset_client: DatasetClient):
        super().__init__(frame_id, "GT", "ADD", dataset_client)

    def _add_crop(self, crop: _BaseCrop) -> None:
        if not isinstance(crop, _Label):
            class_name = self.__class__.__name__
            raise Exception(f"Cannot add {class_name} to a LabeledFrame")
        return super()._add_crop(crop)


Label = Union[
    Bbox2DLabel,
    LineSegment2DLabel,
    Keypoint2DLabel,
    PolygonList2DLabel,
    Semseg2DLabel,
    InstanceSeg2DLabel,
    Classification2DLabel,
    Classification3DLabel,
    Cuboid3DLabel,
    TextTokenLabel,
]


def _get_single_label_from_json(label_json: Dict[str, Any]) -> Label:
    iscrowd = label_json["attributes"].pop("iscrowd", None)
    label_type = label_json["label_type"]
    # instantiate base sensor directly & cast to the right class
    base_label = _BaseSingleCrop(
        id=label_json["uuid"],
        update_type="ADD",
        label_type=label_json["label_type"],
        classification=label_json["label"],
        sensor_id=label_json["label_coordinate_frame"],
        iscrowd=iscrowd,
        attributes=label_json["attributes"],
    )

    if label_type == "BBOX_2D":
        return cast(Bbox2DLabel, base_label)
    elif label_type == "LINE_SEGMENT_2D":
        return cast(LineSegment2DLabel, base_label)
    elif label_type == "KEYPOINTS_2D":
        return cast(Keypoint2DLabel, base_label)
    elif label_type == "POLYGON_LIST_2D":
        return cast(PolygonList2DLabel, base_label)
    elif label_type == "SEMANTIC_LABEL_URL_2D":
        return cast(Semseg2DLabel, base_label)
    elif label_type == "CLASSIFICATION_2D":
        return cast(Classification2DLabel, base_label)
    elif label_type == "CLASSIFICATION_3D":
        return cast(Classification3DLabel, base_label)
    elif label_type == "CUBOID_3D":
        return cast(Cuboid3DLabel, base_label)
    elif label_type == "TEXT_TOKEN":
        return cast(TextTokenLabel, base_label)
    else:
        raise Exception(f"Cannot reinstantiate a label of type {label_type}")


def _get_instance_seg_label_from_jsons(
    mask_json: Dict[str, Any],
    instances: List[Dict[str, Any]],
) -> InstanceSeg2DLabel:
    instantiated_instances = []
    for ins in instances:
        id: int = ins["attributes"].pop("id")
        instantiated_instances.append(
            InstanceSegInstance(id, ins["classification"], ins["attributes"])
        )
    label = InstanceSeg2DLabel(
        id=mask_json["uuid"],
        sensor_id=mask_json["label_coordinate_frame"],
        instances=instantiated_instances,
        **mask_json["attributes"],
    )
    return label
