
        # AMD-Xilinx Vivado project start and tcl script: Create project, xc7z020clg400-1 technology, VHDL model 

        # To execute, 

        # open cmd window 

        # cd to project folder 

        # start Vivado (with tcl file parameter) 

        # e.g, for project name numOf1sInByte 

        # cmd 

        # cd E:/BE_Project/Project/Project_files/HDLGen_files/HDLGen/User_Projects/numOf1sInByte 

        # $vivado_bat_path -source E:/BE_Project/Project/Project_files/HDLGen_files/HDLGen/User_Projects/numOf1sInByte\VHDL\AMDPrj\numOf1sInByte.tcl 


        # Vivado tcl file numOf1sInByte.tcl, created in AMDprj folder 

        cd E:/BE_Project/Project/Project_files/HDLGen_files/HDLGen/User_Projects/numOf1sInByte 

        # Close_project  Not required. Will advise that Vivado sessions should be closed. 

        start_gui

        create_project  numOf1sInByte  ./VHDL/AMDprj -part xc7z020clg400-1 -force

        set_property target_language VHDL [current_project]

        add_files -norecurse  ./VHDL/model/numOf1sInByte.vhd

        update_compile_order -fileset sources_1

        set_property SOURCE_SET sources_1 [get_filesets sim_1]

        add_files -fileset sim_1 -norecurse ./VHDL/testbench/numOf1sInByte_tb.vhd

        update_compile_order -fileset sim_1

    