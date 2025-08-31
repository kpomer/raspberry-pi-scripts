package metrics

import (
	"fmt"
	"os/exec"
	"strings"
)

func GetHelloWorld(sampleData bool) string {

	var returnVal string
	if sampleData {
		// return sample data
		returnVal = getSampleHelloWorld()
	} else {
		// cmd: echo Hello World - REAL
		cmdOutput, err := exec.Command("echo", "Hello World - REAL").Output()
        if err != nil {
            fmt.Println("Error running command:", err)
			returnVal = ""
        } else {
			returnVal = strings.TrimSpace(string(cmdOutput)) // convert []byte to string
		}
		
	}

	return returnVal

}


func getSampleHelloWorld() string {

	return "Hello World! - SAMPLE"

}