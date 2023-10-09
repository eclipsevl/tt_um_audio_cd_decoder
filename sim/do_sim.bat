vlib work
vlog -reportprogress 300 ./*.v 
vsim tb -voptargs=+acc -wlf wave.wlf