
        # AMD-Xilinx Vivado project start and tcl script: Create project, xc7z020clg400-1 technology, VHDL model 

        # To execute, 

        # open cmd window 

        # cd to project folder 

        # start Vivado (with tcl file parameter) 

        # e.g, for project name mux21_1 

        # cmd 

        # cd {C:/Users/User/HDLGen/User_Projects/mux21_1} 

        # $vivado_bat_path -source C:/Users/User/HDLGen/User_Projects/mux21_1/VHDL/AMDPrj/mux21_1.tcl 


        # Vivado tcl file mux21_1.tcl, created in AMDprj folder 

        cd {C:/Users/User/HDLGen/User_Projects/mux21_1} 

        # Close_project  Not required. Will advise that Vivado sessions should be closed. 

        start_gui

        create_project  mux21_1  ./VHDL/AMDprj -part xc7z020clg400-1 -force

        set_property target_language VHDL [current_project]

        add_files -norecurse  ./VHDL/model/mux21_1.vhd


        update_compile_order -fileset sources_1

        set_property SOURCE_SET sources_1 [get_filesets sim_1]

        add_files -fileset sim_1 -norecurse ./VHDL/testbench/mux21_1_tb.vhd

        update_compile_order -fileset sim_1

    