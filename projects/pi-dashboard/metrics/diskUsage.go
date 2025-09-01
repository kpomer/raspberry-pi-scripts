package metrics

import (
	"fmt"
	"os/exec"
	"strings"
)

func GetDiskUsage(sampleData bool) [][]string {

	var val_Str string
	if sampleData {
		// return sample data
		val_Str = getSampleDiskUsage()
	} else {
		// cmd: df -h / /mnt/timemachine /boot/firmware 2>/dev/null
		cmdOutput, err := exec.Command("sh", "-c", "df -h / /mnt/timemachine /boot/firmware 2>/dev/null").Output()
		val_Str = strings.TrimSpace(string(cmdOutput)) // convert []byte to string (ignore errors)
        if err != nil {
            fmt.Println("Error running command:", err)
        }
	}

		val_Str = strings.Replace(val_Str, "Mounted on", "Mounted_On", -1)

		duStr_Lines := strings.Split(val_Str, "\n")


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


func getSampleDiskUsage() string {

	// COMMAND: df -h /
	// SAMPLE RESPONSE:
	// Filesystem      Size  Used Avail Use% Mounted on
	// /dev/mmcblk0p2   59G  2.6G   53G   5% /
	
	duStr := "Filesystem      Size  Used Avail Use% Mounted on\n/dev/mmcblk0p2   59G  2.6G   53G   5% /\n/dev/mmcblk0p8   75G  32.5G   90G   30% /mnt"
	return duStr

}
