A bunch of CSV files recording the bluetooth signal value.

The old format is,
* The first row is a single value to represent the real distance.
* The following rows are received signal and the distance read from 3party sdk, which is not used at all.

The file name is in the format of 
* [uuid]-[major version]-[minor version]-[filter].csv (the "filter" key words is optional, which indicates whether the signal get filtered or not.)

The new format is, an example given below,
{
	"period":60,
	"interestedBeacons":[{"proximityUUID":"B9407F30F5F8466EAFF925556B57FE6D",
						  "major":24778,
						  "minor":11294,
						  "realDistance":1,
						  "rssis":[]}], 
	"startTime":"2014-05-09T12:02:48.718Z",
	"endTime":"2014-05-09T13:02:48.758Z"
}
