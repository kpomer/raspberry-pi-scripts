package metrics

import (
	"fmt"
	"os/exec"
	"strings"
)

func GetUptime(sampleData bool) string {

	var returnVal string
	if sampleData {
		// return sample data
		returnVal = getSampleUptime()
	} else {
		// cmd: uptime -p
		cmdOutput, err := exec.Command("uptime", "-p").Output()
        if err != nil {
            fmt.Println("Error running command:", err)
			returnVal = ""
        } else {
			returnVal = strings.TrimSpace(string(cmdOutput)) // convert []byte to string
		}
		
	}

	return returnVal

}


func getSampleUptime() string {

	return "up 1 day, 1 hour, 23 minutes"

}