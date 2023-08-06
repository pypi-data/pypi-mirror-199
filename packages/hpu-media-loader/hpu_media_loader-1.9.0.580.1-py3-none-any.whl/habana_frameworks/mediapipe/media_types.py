# data type supported
class dtype:
    """
    Class defining media data types supported.

    """
    NDT = ""
    UINT8 = "uint8"
    UINT16 = "uint16"
    UINT32 = "uint32"
    UINT64 = "uint64"
    INT8 = "int8"
    INT16 = "int16"
    INT32 = "int32"
    INT64 = "int64"
    FLOAT16 = "float16"
    BFLOAT16 = "bfloat16"
    FLOAT32 = "float32"


# filter types
class ftype:
    """
    Class defining media decoder filters supported.

    """
    LINEAR = 0
    LANCZOS = 1
    NEAREST = 2
    BI_LINEAR = 3
    BICUBIC = 4
    SPLINE = 5
    BOX = 6


# layout types
class layout:
    """
    Class defining media layout supported.

    """
    NA = ""   # interleaved
    NHWC = "CWHN"   # interleaved
    NCHW = "WHCN"   # planar
    FHWC = "CWHC"   # video


# image type
class imgtype:
    """
    Class defining media decoder image types supported.

    """
    RGB_I = "rgb-i"
    RGB_P = "rgb-p"


class readerOutType:
    """
    Class defining media reader output type.

    """
    FILE_LIST = 0
    BUFFER_LIST = 1
    ADDRESS_LIST = 2


class randomCropType:
    """
    Class defining media random crop types.

    """
    NO_RANDOM_CROP = "no_crop"
    RANDOMIZED_AREA_AND_ASPECT_RATIO_CROP = "randomized_area_and_aspect_ratio_crop"
    RANDOMIZED_ASPECT_RATIO_CROP = "randomized_aspect_ratio_crop"
    CENTER_CROP = "center_crop"


class decoderStage:
    """
    Class defining media decoder stages.

    """
    ENABLE_ALL_STAGES = "all_stages"
    ENABLE_SINGLE_STAGE = "single_stage"
    ENABLE_TWO_STAGES = "two_stages"


class decoderType:
    """
    Class defining media decoder types.

    """
    IMAGE_DECODER = "image_decoder"
    VIDEO_DECODER = "video_decoder"
