# HDLGen application
- HDLGen is an open-source client application, developed by the Vicilogic team.
Vicilogic is an online learning, assessment, remote FPGA prototying and coure builder platform [vicilogic.com](https://www.vicilogic.com)

- Many students find it difficult to learn 
	- digital design concepts
	- hardware description language (HDL) modelling and testbenching
	- complex EDA tools used for HDL simulation, synthesis, and FPGA prototyping. 

- HDLGen provides a wizard for fast, automated 
	- Creation of System on Chip (SoC) hardware description language (HDL) model templates
	- HDL testbench template
	- Electronic Design Automation (EDA) tool project folders, files and TCL scripts
	- EDA toolsuite projects 
	- Tool Command Language (TCL) scripts

- HDLGen generates VHDL to the level of concurrent statement and process level case statement description, VHDL testbench and Vivado project, i.e, 
	- VHDL model header, component and signal descriptions
	- VHDL library (including project package) 
	- Design component entity
	- Design component architecture
		- internal signal declarations
		- process and concurrent statement templates

- HDLGen uses graphical component design documentation (typically used in Vicilogic lessons), including 
	- component symbol (context diagram)
	- input/output signals
	- signal dictionary (SD)
	- data flow diagrams (DFDs)
	- process descriptions (PDs)
	- internal signals
	- default assignment
	- incremental PDs and SDs
	- two process Finite State Machine (FSM)-based models. 

# HDLGen supports teaching
- HDLGen can be used to support teaching of digital systems and computer architecture design, 
Vicilogic (https://vicilogic.com) lessons reference the use of HDLGen.
- [1] demonstrates the use of HDLGen for creation of a range of combinational and sequential design projects. 

- Feedback from students confirms that HDLGen enables faster and more clear and accurate generation of VHDL component models than those created manually. 
Some proprietary EDA tools (typically subscription-based) provide graphical design entry and support for automated HDL capture and syntax checking, though these tools are not widely available. 

# HDLGen current support
- AMD Xilinx Vivado V2019.1 FPGA EDA toolsuite [2]
- VHDL

# HDLGen future support (in development)
- Intel Quartus V21.1.1.850 FPGA EDA toolsuite [3]
- Verilog
- 
## Created by 
Fearghal Morgan, Abishek Bupathi and John Patrick Byrne 
- University of Galway, Ireland
- [vicilogic.com](https://www.vicilogic.com)

## HDLGen download and installation
- [HDLGen github repository](https://github.com/abishek-bupathi/HDLGen)

## [Contact Us](mailto:fearghal.morgan1@gmail.ie?subject=HDLGen-ChatGPT email) with comments and/or suggestions

## EDA toolsuite download links

[1] Demonstrators for "Vicilogic: Linking Online Learning Assessment and Prototyping with Remote FPGA Hardware" <https://www.vicilogic.com/vicilearn/run_step/?c_id=69>

[2] [AMD Xilinx Vivado free webpack version 2019.1 (windows)](https://www.xilinx.com/member/forms/download/xef-vivado.html?filename=Xilinx_Vivado_SDK_Web_2019.1_0524_1430_Win64.exe)

[3] [Intel Quartus version 21.1.1.850 (windows)](https://www.intel.com/content/www/us/en/software-kit/736595/intel-quartus-prime-standard-edition-design-software-version-21-1-1-for-windows.html)