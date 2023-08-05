[drip_drip](https://gitlab.com/nest.lbl.gov/drip_drip) contains the python package that provides a utility to controls automatic movment of files from one directory to another such that:

* the rate of copying can be throttled; and

* the number of files in the destination directory can be limited, so that it does not become overly large.

The package includes the `drip_feed` command which can be used to execute the utility. The command take the name of a `Dropper` plug-in that assess whether there is sufficient space at the destination and when there is the plug-in will also manage the movement of the files. The plug-in can also be specified in the environmental variable `DRIP_DROPPER` but any value specified in this variable will be ignored if an argument is provided to the `drip_feed` command.

Full details for configuring the command can be found [here](web/docs/configuration.md).
