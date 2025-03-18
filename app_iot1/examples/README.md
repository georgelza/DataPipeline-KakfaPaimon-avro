# Examples

- Base Payload

```json5
{
	"timestamp" : "2024-10-02T01:00:00.869Z",
	"metadata" : {
		"siteId" : 1009,
		"deviceId" : 1042,
		"sensorId" : 10180,
		"unit" : "Psi"
	},
	"measurement" : 1015.3997
}
```

- Modified Payload

```json5
{
	"timestamp" : "2024-10-02T01:00:00.869Z",
	"metadata" : {
		"siteId" : 1009,
		"deviceId" : 1042,
		"sensorId" : 10180,
		"unit" : "Psi",
		"location":{
			"latitude": 23452,
			"longitude": 02342
		}
	},
	"measurement" : 1015.3997
}
```

