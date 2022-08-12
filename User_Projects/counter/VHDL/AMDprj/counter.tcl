
        # AMD-Xilinx Vivado project start and tcl script: Create project, xc7z020clg400-1 technology, VHDL model 

        # To execute, 

        # open cmd window 

        # cd to project folder 

        # start Vivado (with tcl file parameter) 

        # e.g, for project name counter 

        # cmd 

        # cd E:\BE_Project\Project\Project_files\HDLGen_files\HDLGen\User_Projects/counter 

        # $vivado_bat_path -source E:\BE_Project\Project\Project_files\HDLGen_files\HDLGen\User_Projects/counter\VHDL\AMDPrj\counter.tcl 


        # Vivado tcl file counter.tcl, created in AMDprj folder 

        cd E:\BE_Project\Project\Project_files\HDLGen_files\HDLGen\User_Projects/counter 

        # Close_project  Not required. Will advise that Vivado sessions should be closed. 

        start_gui

        create_project  counter  ./VHDL/AMDprj -part xc7z020clg400-1 -force

        set_property target_language VHDL [current_project]

        add_files -norecurse  ./VHDL/model/counter.vhd

        update_compile_order -fileset sources_1

        set_property SOURCE_SET sources_1 [get_filesets sim_1]

        add_files -fileset sim_1 -norecurse ./VHDL/testbench/counter_tb.vhd

        update_compile_order -fileset sim_1

    