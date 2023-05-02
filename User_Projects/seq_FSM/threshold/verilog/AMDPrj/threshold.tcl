
        # AMD-Xilinx Vivado project start and tcl script: Create project, xc7z020clg400-1 technology, %lang model 

        # To execute, 

        # open cmd window 

        # cd to project folder 

        # start Vivado (with tcl file parameter) 

        # e.g, for project name threshold 

        # cmd 

        # cd {C:/2023/vicilogic/HDLGenTop/HDLGen/User_Projects/seq_FSM/threshold} 

        # $vivado_bat_path -source C:/2023/vicilogic/HDLGenTop/HDLGen/User_Projects/seq_FSM/threshold/Verilog/AMDPrj/threshold.tcl 


        # Vivado tcl file threshold.tcl, created in AMDprj folder 

        cd {C:/2023/vicilogic/HDLGenTop/HDLGen/User_Projects/seq_FSM/threshold} 

        # Close_project  Not required. Will advise that Vivado sessions should be closed. 

        start_gui

        create_project  threshold  ./Verilog/AMDprj -part xc7z020clg400-1 -force

        set_property target_language Verilog [current_project]

        add_files -norecurse  ./Verilog/model/threshold.v

add_files -norecurse  C:/2023/vicilogic/HDLGenTop/HDLGen/User_Projects/memory/reg4x4/VHDL/model/reg4x4.vhd 
add_files -norecurse  C:/2023/vicilogic/HDLGenTop/HDLGen/User_Projects/combinational/mux21_1/VHDL/model/mux21_1.vhd 
add_files -norecurse  C:/2023/vicilogic/HDLGenTop/HDLGen/User_Projects/combinational/mux21_4/VHDL/model/mux21_4.vhd 
add_files -norecurse  C:/2023/vicilogic/HDLGenTop/HDLGen/User_Projects/memory/reg4x4/VHDL/model/reg4x4.vhd 
add_files -norecurse  C:/2023/vicilogic/HDLGenTop/HDLGen/User_Projects/combinational/mux21_1/VHDL/model/mux21_1.vhd 
add_files -norecurse  C:/2023/vicilogic/HDLGenTop/HDLGen/User_Projects/combinational/mux21_4/VHDL/model/mux21_4.vhd 


        update_compile_order -fileset sources_1

        set_property SOURCE_SET sources_1 [get_filesets sim_1]

        add_files -fileset sim_1 -norecurse ./Verilog/testbench/threshold_TB.v

        update_compile_order -fileset sim_1

        # Remove IOBs from snthesised schematics

        current_run [get_runs synth_1]

        set_property -name {STEPS.SYNTH_DESIGN.ARGS.MORE OPTIONS} -value -no_iobuf -objects [get_runs synth_1]


        # Save created wcfg in project

        set_property SOURCE_SET sources_1 [get_filesets sim_1]

        add_files -fileset sim_1 -norecurse ./Verilog/AMDPrj/threshold_TB_behav.wcfg

        # save_wave_config {./Verilog/AMDprj/threshold_TB_behav.wcfg}

    