
        # AMD-Xilinx Vivado project start and tcl script: Create project, xc7z020clg400-1 technology, VHDL model 

        # To execute, 

        # open cmd window 

        # cd to project folder 

        # start Vivado (with tcl file parameter) 

        # e.g, for project name SReg4 

        # cmd 

        # cd E:/BE_Project/Project/Project_files/HDLGen_files/HDLGen/User_Projects/SReg4 

        # $vivado_bat_path -source E:/BE_Project/Project/Project_files/HDLGen_files/HDLGen/User_Projects/SReg4\VHDL\AMDPrj\SReg4.tcl 


        # Vivado tcl file SReg4.tcl, created in AMDprj folder 

        cd E:/BE_Project/Project/Project_files/HDLGen_files/HDLGen/User_Projects/SReg4 

        # Close_project  Not required. Will advise that Vivado sessions should be closed. 

        start_gui

        create_project  SReg4  ../VHDL/AMDprj -part xc7z020clg400-1 -force

        set_property target_language VHDL [current_project]

        add_files -norecurse  ./VHDL/model/SReg4.vhd

        update_compile_order -fileset sources_1

        set_property SOURCE_SET sources_1 [get_filesets sim_1]

        