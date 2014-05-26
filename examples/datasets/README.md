A bunch of CSV files recording the bluetooth signal value.

The format is,
* The first row is a single value to represent the real distance.
* The following rows are received signal and the distance read from 3party sdk, which is not used at all.

The file name is in the format of 
* <uuid>-<major version>-<minor version>-[filter].csv (the "filter" key words indicate whether the signal get filtered or not.)