#######################################################################################################################
#
#
#  	Project     	    : 	IoT based TimeSeries Data via Python Application 
#
#   File                :   main.py
#
#   Description         :   Mostly polishing and optimizing. See the various sub *.py files.
#
#   Created     	    :   22 November 2024
#
#
#   JSON Viewer         :   https://jsonviewer.stack.hu
#
#   Mongodb             :   https://www.mongodb.com/cloud/atlas      
#                       :   https://hub.docker.com/r/mongodb/mongodb-atlas-local
#
#   Create Virtualenv   :   python3 -m venv ./venv
#
########################################################################################################################

__author__      = "George Leonard"
__email__       = "georgelza@gmail.com"
__version__     = "3.0.0"
__copyright__   = "Copyright 2024, - G Leonard"


import utils
import simulate
import os, multiprocessing
from datetime import datetime


def main():
    
    
    # For those noticing, we're modifying the LOGGINGFILE value a bit, the end result is that each run will have a unique logfile
    # based on LOGGINGFILE and the current runtime, 
    # this is because we want to keep the logs for each run, so that we can see how the program is running.

    runTime                      = str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
    config_params                = utils.configparams()
    config_params["LOGGINGFILE"] = config_params["LOGDIR"] + "/"+ config_params["LOGGINGFILE"] + "_" + runTime
    config_params["FILEROOT"]    = config_params["LOGDIR"] + "/"+ config_params["FILEROOT"] + "_" + runTime
    logger                       = utils.logger(config_params["LOGGINGFILE"] + "_common.log", config_params["CONSOLE_DEBUGLEVEL"], config_params["FILE_DEBUGLEVEL"])

    logger.info("STARTING run, logfile => {logfile}".format(
        logfile=config_params["LOGGINGFILE"]
    ))


    utils.echo_config(config_params, logger)
        
        
    # Load the Entire SeedFile
    my_seedfile = utils.read_seed_file(config_params, logger)
    if my_seedfile == -1 :
        os._exit(1)
        
    # end if


    # Load site data and start simulation for each siteId
    my_sites = []
    for siteId in config_params["SITEIDS"]:
        
        cur_site = utils.find_site(my_seedfile, int(siteId), logger)
        if cur_site == -1:
            os._exit(1)
                    
        # end if
        my_sites.append(cur_site)
        
    current_time = datetime.now()

    # Create processes for each site
    processes = []
    
    logger.info("")
    try:
        for site in my_sites:
            
            siteLabel = "SiteId: " + str(site["siteId"])
            
            logger.info("Calling simulate.run_simulation for {siteLabel}".format(
                siteLabel=siteLabel
            ))
            
            # Create a process for each site
            p = multiprocessing.Process(target=simulate.run_simulation, name=siteLabel, args=(site, current_time, config_params))
            processes.append(p)
            p.start()

        # end for

        for p in processes:
            p.join()
            
        # end for
            
    except KeyboardInterrupt:
        
        logger.warning("KeyboardInterrupt detected! Terminating all processes...")
        logger.warning("")
        
        # Terminate all running processes if Ctrl+C is pressed
        for p in processes:
            p.terminate()
            p.join()

        logger.info("All processes terminated. Exiting gracefully...")

    # end try
                    
    logger.info("COMPLETED run, logfile  - {logfile}".format(
        logfile=config_params["LOGGINGFILE"]
    ))

# end main


if __name__ == "__main__":

    main()
    
# END ...