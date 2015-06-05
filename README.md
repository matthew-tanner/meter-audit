## Meter Audit

MA is a small web scraping tool (proof of concept) for a specific task related to printer meter readings. It is for use when FMAudit cannot be used in an OSX based network environment, where meter counts are required to be obtained on a recurring basis.

The script will connect to all given IPs related to the printers and pull meter readings from each one. It will then email (Gmail Support Only) the list of meters to the provided address for review.

## Printers Supported

Currently only Konica Minolta 4700p / 3060 printers are supported. This is due to the Xpath information being hard coded into the script and no dynamic searth features are implemented to allow a wider range of printers.

## Settings

+ iplist_example.txt - rename to iplist.txt , must contain only IP addresses (no comments / wording)
+ settings_example.conf - rename to settings.conf , update settings with your specific information

## Future Plans

I have no future plans for this other than it being a proof of concept for being an alternative to FMAudit in a business environment.
