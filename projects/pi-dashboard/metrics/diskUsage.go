package metrics

import "strings"

func GetDiskUsage(sampleData bool) [][]string {


	if sampleData {
		// return sample data
		return getSampleDiskUsage()
	}



	// TODO Retrieve Actual Data
	// COMMAND: df -h /
	// SAMPLE RESPONSE:
	// Filesystem      Size  Used Avail Use% Mounted on
	// /dev/mmcblk0p2   59G  2.6G   53G   5% /
	
	
	duStr := "Filesystem      Size  Used Avail Use% Mounted on\n/dev/mmcblk0p2   59G  2.6G   53G   5% /\n/dev/mmcblk0p8   75G  32.5G   90G   30% /mnt"
	duStr = strings.Replace(duStr, "Mounted on", "Mounted_On", -1)

	duStr_Lines := strings.Split(duStr, "\n")


	var diskUsageTable [][]string
	for _, line := range duStr_Lines {
		
		// strings.Fields() handles any amount of whitespace
		strArr := strings.Fields(line)
		if len(strArr) > 0 { // Avoid appending empty slices if a line is just whitespace
			diskUsageTable = append(diskUsageTable, strArr)
		}
	}

	return diskUsageTable

}


func getSampleDiskUsage() [][]string {


	// TODO Retrieve Actual Data
	// COMMAND: df -h /
	// SAMPLE RESPONSE:
	// Filesystem      Size  Used Avail Use% Mounted on
	// /dev/mmcblk0p2   59G  2.6G   53G   5% /
	
	
	duStr := "Filesystem      Size  Used Avail Use% Mounted on\n/dev/mmcblk0p2   59G  2.6G   53G   5% /\n/dev/mmcblk0p8   75G  32.5G   90G   30% /mnt"
	duStr = strings.Replace(duStr, "Mounted on", "Mounted_On", -1)

	duStr_Lines := strings.Split(duStr, "\n")


	var diskUsageTable [][]string
	for _, line := range duStr_Lines {
		
		// strings.Fields() handles any amount of whitespace
		strArr := strings.Fields(line)
		if len(strArr) > 0 { // Avoid appending empty slices if a line is just whitespace
			diskUsageTable = append(diskUsageTable, strArr)
		}
	}

	return diskUsageTable

}