#
# Default configuration for CLI tools
#

# Default configuration for "bootstrap" command
from nabu.stitching.config import StitchingType


BootstrapConfig = {
    "bootstrap": {
        "help": "DEPRECATED, this is the default behavior. Bootstrap a configuration file from scratch.",
        "action": "store_const",
        "const": 1,
    },
    "convert": {
        "help": "UNSUPPORTED. This option has no effect and will disappear. Convert a PyHST configuration file to a nabu configuration file.",
        "default": "",
    },
    "output": {
        "help": "Output filename",
        "default": "nabu.conf",
    },
    "nocomments": {
        "help": "Remove the comments in the configuration file (default: False)",
        "action": "store_const",
        "const": 1,
    },
    "level": {
        "help": "Level of options to embed in the configuration file. Can be 'required', 'optional', 'advanced'.",
        "default": "optional",
    },
    "dataset": {
        "help": "Pre-fill the configuration file with the dataset path.",
        "default": "",
    },
    "template": {
        "help": "Use a template configuration file. Available are: id19_pag, id16_holo, id16_ctf. You can also define your own templates via the NABU_TEMPLATES_PATH environment variable.",
        "default": "",
    },
    "helical": {"help": "Prepare configuration file for helical", "default": 0, "required": False, "type": int},
}

# Default configuration for "zsplit" command
ZSplitConfig = {
    "input_file": {
        "help": "Input HDF5-Nexus file",
        "mandatory": True,
    },
    "output_directory": {
        "help": "Output directory to write split files.",
        "mandatory": True,
    },
    "loglevel": {
        "help": "Logging level. Can be 'debug', 'info', 'warning', 'error'. Default is 'info'.",
        "default": "info",
    },
    "entry": {
        "help": "HDF5 entry to take in the input file. By default, the first entry is taken.",
        "default": "",
    },
    "n_stages": {
        "help": "Number of expected stages (i.e different 'Z' values). By default it is inferred from the dataset.",
        "default": -1,
        "type": int,
    },
    "use_virtual_dataset": {
        "help": "Whether to use virtual datasets for output file. Not using a virtual dataset duplicates data and thus results in big files ! However virtual datasets currently have performance issues. Default is False",
        "default": 0,
        "type": int,
    },
}

# Default configuration for "histogram" command
HistogramConfig = {
    "h5_file": {
        "help": "HDF5 file(s). It can be one or several paths to HDF5 files. You can specify entry for each file with /path/to/file.h5?entry0000",
        "mandatory": True,
        "nargs": "+",
    },
    "output_file": {
        "help": "Output file (HDF5)",
        "mandatory": True,
    },
    "bins": {
        "help": "Number of bins for histogram if they have to be computed. Default is one million.",
        "default": 1000000,
        "type": int,
    },
    "chunk_size_slices": {
        "help": "If histogram are computed, specify the maximum subvolume size (in number of slices) for computing histogram.",
        "default": 100,
        "type": int,
    },
    "chunk_size_GB": {
        "help": "If histogram are computed, specify the maximum subvolume size (in GibaBytes) for computing histogram.",
        "default": -1,
        "type": float,
    },
    "loglevel": {
        "help": "Logging level. Can be 'debug', 'info', 'warning', 'error'. Default is 'info'.",
        "default": "info",
    },
}


# Default configuration for "reconstruct" command
ReconstructConfig = {
    "input_file": {
        "help": "Nabu input file",
        "default": "",
        "mandatory": True,
    },
    "logfile": {
        "help": "Log file. Default is dataset_prefix_nabu.log",
        "default": "",
    },
    "log_file": {
        "help": "Same as logfile. Deprecated, use --logfile instead.",
        "default": "",
    },
    "slice": {
        "help": "Slice(s) indice(s) to reconstruct, in the format z1-z2. Default (empty) is the whole volume. This overwrites the configuration file start_z and end_z. You can also use --slice first, --slice last, --slice middle, and --slice all",
        "default": "",
    },
    "gpu_mem_fraction": {
        "help": "Which fraction of GPU memory to use. Default is 0.9.",
        "default": 0.9,
        "type": float,
    },
    "cpu_mem_fraction": {
        "help": "Which fraction of memory to use. Default is 0.9.",
        "default": 0.9,
        "type": float,
    },
    "max_chunk_size": {
        "help": "Maximum chunk size to use.",
        "default": -1,
        "type": int,
    },
    "phase_margin": {
        "help": "Specify an explicit phase margin to use when performing phase retrieval.",
        "default": -1,
        "type": int,
    },
    "force_use_grouped_pipeline": {
        "help": "Force nabu to use the 'grouped' reconstruction pipeline - slower but should work for all big datasets.",
        "default": 0,
        "type": int,
    },
}

GenerateInfoConfig = {
    "hist_file": {
        "help": "HDF5 file containing the histogram, either the reconstruction file or a dedicated histogram file.",
        "default": "",
    },
    "hist_entry": {
        "help": "Histogram HDF5 entry. Defaults to the first available entry.",
        "default": "",
    },
    "output": {
        "help": "Output file name",
        "default": "",
        "mandatory": True,
    },
    "bliss_file": {
        "help": "HDF5 master file produced by BLISS",
        "default": "",
    },
    "bliss_entry": {
        "help": "Entry in the HDF5 master file produced by BLISS. By default, take the first entry.",
        "default": "",
    },
    "info_file": {
        "help": "Path to the .info file, in the case of a EDF dataset",
        "default": "",
    },
    "edf_proj": {
        "help": "Path to a projection, in the case of a EDF dataset",
        "default": "",
    },
}

RotateRadiosConfig = {
    "dataset": {
        "help": "Path to the dataset. Only HDF5 format is supported for now.",
        "default": "",
        "mandatory": True,
    },
    "entry": {
        "help": "HDF5 entry. By default, the first entry is taken.",
        "default": "",
    },
    "angle": {
        "help": "Rotation angle in degrees",
        "default": 0.0,
        "mandatory": True,
        "type": float,
    },
    "center": {
        "help": "Rotation center, in the form (x, y) where x (resp. y) is the horizontal (resp. vertical) dimension, i.e along the columns (resp. lines). Default is (Nx/2 - 0.5, Ny/2 - 0.5).",
        "default": "",
    },
    "output": {
        "help": "Path to the output file. Only HDF5 output is supported. In the case of HDF5 input, the output file will have the same structure.",
        "default": "",
        "mandatory": True,
    },
    "loglevel": {
        "help": "Logging level. Can be 'debug', 'info', 'warning', 'error'. Default is 'info'.",
        "default": "info",
    },
    "batchsize": {
        "help": "Size of the batch of images to process. Default is 100",
        "default": 100,
        "type": int,
    },
    "use_cuda": {
        "help": "Whether to use Cuda if available",
        "default": "1",
    },
    "use_multiprocessing": {
        "help": "Whether to use multiprocessing if available",
        "default": "1",
    },
}

DFFConfig = {
    "dataset": {
        "help": "Path to the dataset.",
        "default": "",
        "mandatory": True,
    },
    "entry": {
        "help": "HDF5 entry (for HDF5 datasets). By default, the first entry is taken.",
        "default": "",
    },
    "flatfield": {
        "help": "Whether to perform flat-field normalization. Default is True.",
        "default": "1",
        "type": int,
    },
    "sigma": {
        "default": 0.0,
        "help": "Enable high-pass filtering on double flatfield with this value of 'sigma'",
        "type": float,
    },
    "output": {
        "help": "Path to the output file (HDF5).",
        "default": "",
        "mandatory": True,
    },
    "loglevel": {
        "help": "Logging level. Can be 'debug', 'info', 'warning', 'error'. Default is 'info'.",
        "default": "info",
    },
    "chunk_size": {
        "help": "Maximum number of lines to read in each projection in a single pass. Default is 100",
        "default": 100,
        "type": int,
    },
}

CompareVolumesConfig = {
    "volume1": {
        "help": "Path to the first volume.",
        "default": "",
        "mandatory": True,
    },
    "volume2": {
        "help": "Path to the first volume.",
        "default": "",
        "mandatory": True,
    },
    "entry": {
        "help": "HDF5 entry. By default, the first entry is taken.",
        "default": "",
    },
    "hdf5_path": {
        "help": "Full HDF5 path to the data. Default is <entry>/reconstruction/results/data",
        "default": "",
    },
    "chunk_size": {
        "help": "Maximum number of images to read in each step. Default is 100.",
        "default": 100,
        "type": int,
    },
    "stop_at": {
        "help": "Stop the comparison immediately when the difference exceeds this threshold. Default is to compare the full volumes.",
        "default": "1e-4",
    },
    "statistics": {
        "help": "Compute statistics on the compared (sub-)volumes. Mind that in this case the command output will not be empty!",
        "default": 0,
        "type": int,
    },
}


# Default configuration for "stitching" command
StitchingConfig = {
    "input_file": {
        "help": "Nabu configuraiton file for stitching (can be obtain from nabu-stitching-boostrap command)",
        "default": "",
        "mandatory": True,
    },
    "loglevel": {
        "help": "Logging level. Can be 'debug', 'info', 'warning', 'error'. Default is 'info'.",
        "default": "info",
    },
}

# Default configuration for "stitching-bootstrap" command
BootstrapStitchingConfig = {
    "stitching_type": {
        "help": f"User can provide stitching type to filter some parameters. Must be in {StitchingType.values()}.",
        "default": None,
    },
    "level": {
        "help": "Level of options to embed in the configuration file. Can be 'required', 'optional', 'advanced'.",
        "default": "optional",
    },
    "output": {
        "help": "output file to store the configuration",
        "default": "stitching.conf",
    },
}


ShrinkConfig = {
    "input_file": {
        "help": "Path to the NX file",
        "default": "",
        "mandatory": True,
    },
    "output_file": {
        "help": "Path to the output NX file",
        "default": "",
        "mandatory": True,
    },
    "entry": {
        "help": "HDF5 entry in the file. Default is to take the first entry.",
        "default": "",
    },
    "binning": {
        "help": "Binning factor, in the form (bin_z, bin_x). Each image (projection, dark, flat) will be binned by this factor",
        "default": "",
    },
    "subsampling": {"help": "Subsampling factor for projections (and metadata)", "default": ""},
    "threads": {
        "help": "Number of threads to use for binning. Default is 1.",
        "default": 1,
        "type": int,
    },
}

CompositeCorConfig = {
    "--filename_template": {
        "required": True,
        "help": """The filename template. It can optionally contain a segment equal to "X"*ndigits which will be replaced by the stage number if several stages are requested by the user""",
    },
    "--entry_name": {
        "required": False,
        "help": "Optional. The entry_name. It defaults to entry0000",
        "default": "entry0000",
    },
    "--num_of_stages": {
        "type": int,
        "required": False,
        "help": "Optional. How many stages. Example: from 0 to 43 -> --num_of_stages  44. It is optional. ",
    },
    "--oversampling": {
        "type": int,
        "default": 4,
        "required": False,
        "help": "Oversampling in the research of the axis position. Defaults to 4 ",
    },
    "--n_subsampling_y": {
        "type": int,
        "default": 10,
        "required": False,
        "help": "How many lines we are going to take from each radio. Defaults to 10.",
    },
    "--theta_interval": {
        "type": float,
        "default": 5,
        "required": False,
        "help": "Angular step for composing the image. Default to 5",
    },
    "--first_stage": {"type": int, "default": None, "required": False, "help": "Optional. The first stage.  "},
    "--output_file": {
        "type": str,
        "required": False,
        "help": "Optional. Where the list of cors will be written. Default is the filename postixed with cors.txt",
    },
    "--cor_options": {
        "type": str,
        "help": """the cor_options string used by Nabu. Example 
        --cor_options "side='near'; near_pos = 300.0;  near_width = 20.0"
        """,
        "required": True,
    },
}

CreateDistortionMapHorizontallyMatchedFromPolyConfig = {
    "--nz": {"type": int, "help": "vertical dimension of the detector", "required": True},
    "--nx": {"type": int, "help": "horizontal dimension of the detector", "required": True},
    "--center_z": {"type": float, "help": "vertical position of the optical center", "required": True},
    "--center_x": {"type": float, "help": "horizontal position of the optical center", "required": True},
    "--c4": {"type": float, "help": "order 4 coefficient", "required": True},
    "--c2": {"type": float, "help": "order 2 coefficient", "required": True},
    "--target_file": {"type": str, "help": "The map output filename", "required": True},
    "--axis_pos": {
        "type": float,
        "default": None,
        "help": "Optional argument. If given it will be corrected for use with the produced map. The value is printed, or given as return argument if the utility is used from a script",
        "required": False,
    },
    "--loglevel": {
        "help": "Logging level. Can be 'debug', 'info', 'warning', 'error'. Default is 'info'.",
        "default": "info",
    },
}
