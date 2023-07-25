-- Package
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
package MainPackage is
type reg4x4_Array is array(3 downto 0) of std_logic_vector(3 downto 0);
type reg4x32_Array is array(3 downto 0) of std_logic_vector(31 downto 0);
type reg32x32_Array is array(31 downto 0) of std_logic_vector(31 downto 0);
type reg4x1_Array is array(3 downto 0) of std_logic_vector(0 downto 0);
type reg1024x32 is array(1023 downto 0) of std_logic_vector(31 downto 0);
type array4x32 is array(3 downto 0) of std_logic_vector(31 downto 0);
type array32x32 is array(31 downto 0) of std_logic_vector(31 downto 0);
type array128x32 is array(127 downto 0) of std_logic_vector(31 downto 0);
type array256x32 is array(255 downto 0) of std_logic_vector(31 downto 0);

component mux21_1 is
port(
	sel : in std_logic;
	muxIn1 : in std_logic;
	muxIn0 : in std_logic;
	muxOut : out std_logic
);
end component mux21_1; 
component mux21_4 is
port(
	mux21_4_In1 : in std_logic_vector(3 downto 0);
	mux21_4_In0 : in std_logic_vector(3 downto 0);
	sel : in std_logic;
	mux21_4_Out : out std_logic_vector(3 downto 0)
);
end component mux21_4; 
component singleShot is
port(
	clk : in std_logic;
	rst : in std_logic;
	sw : in std_logic;
	aShot : out std_logic
);
end component singleShot; 
component memorySys is
port(
	clk : in std_logic;
	rst : in std_logic;
	selMemBankToBeWritten : in std_logic;
	we : in std_logic;
	add : in std_logic_vector(1 downto 0);
	dIn : in std_logic_vector(3 downto 0);
	dOut : out std_logic_vector(3 downto 0);
	ce : in std_logic;
	selMemBankToBeRead : in std_logic
);
end component memorySys; 
component threshold is
port(
	clk : in std_logic;
	rst : in std_logic;
	ce : in std_logic;
	go : in std_logic;
	reg4x32_CSRA : in reg4x32_Array;
	reg4x32_CSRB : in reg4x32_Array;
	BRAM_dOut : in std_logic_vector(255 downto 0);
	active : out std_logic;
	wr : out std_logic;
	add : out std_logic_vector(7 downto 0);
	datToMem : out std_logic_vector(31 downto 0);
	functBus : out std_logic_vector(95 downto 0)
);
end component threshold; 
component CB4CLED is
port(
	clk : in std_logic;
	rst : in std_logic;
	load : in std_logic;
	loadDat : in std_logic_vector(3 downto 0);
	ce : in std_logic;
	up : in std_logic;
	count : out std_logic_vector(3 downto 0);
	TC : out std_logic;
	ceo : out std_logic
);
end component CB4CLED; 
component CB32C_maxCount is
port(
	clk : in std_logic;
	rst : in std_logic;
	ce : in std_logic;
	ceo : out std_logic;
	maxCount : in std_logic_vector(31 downto 0)
);
end component CB32C_maxCount; 
component CB9 is
port(
	clk : in std_logic;
	rst : in std_logic;
	count : out std_logic_vector(8 downto 0)
);
end component CB9; 
component CB32CE is
port(
	clk : in std_logic;
	rst : in std_logic;
	ce : in std_logic;
	TC : out std_logic;
	ceo : out std_logic;
	count : out std_logic_vector(31 downto 0)
);
end component CB32CE; 
component singleShotCE is
port(
	clk : in std_logic;
	rst : in std_logic;
	sw : in std_logic;
	aShot : out std_logic;
	ce : in std_logic
);
end component singleShotCE; 
component multCtrlr is
port(
	clk : in std_logic;
	rst : in std_logic;
	ce : in std_logic;
	goMult : in std_logic;
	initMult : out std_logic;
	multCE : out std_logic;
	multDone : out std_logic;
	multCtrlrStatus : out std_logic_vector(2 downto 0)
);
end component multCtrlr; 
component multiplierDatapath is
port(
	clk : in std_logic;
	rst : in std_logic;
	multiplicand : in std_logic_vector(4 downto 0);
	multiplier : in std_logic_vector(4 downto 0);
	initMult : in std_logic;
	multCE : in std_logic;
	multOut : out std_logic_vector(9 downto 0);
	multiplierDatapathStatus : out std_logic_vector(30 downto 0)
);
end component multiplierDatapath; 
component RISCV_ALU is
port(
	selALUOp : in std_logic_vector(3 downto 0);
	A : in std_logic_vector(31 downto 0);
	B : in std_logic_vector(31 downto 0);
	ALUOut : out std_logic_vector(31 downto 0);
	branch : out std_logic
);
end component RISCV_ALU; 
component RISCV_RB is
port(
	clk : in std_logic;
	rst : in std_logic;
	RWr : in std_logic;
	rd : in std_logic_vector(4 downto 0);
	rs1 : in std_logic_vector(4 downto 0);
	rs2 : in std_logic_vector(4 downto 0);
	rs1D : out std_logic_vector(31 downto 0);
	rs2D : out std_logic_vector(31 downto 0);
	WBDat : in std_logic_vector(31 downto 0);
	ce : in std_logic
);
end component RISCV_RB; 
component RISCV_PCCU is
port(
	clk : in std_logic;
	rst : in std_logic;
	load : in std_logic;
	loadDat : in std_logic_vector(31 downto 0);
	ce : in std_logic;
	count : out std_logic_vector(31 downto 0);
	countPlus4 : out std_logic_vector(31 downto 0)
);
end component RISCV_PCCU; 
component RISCV_IF is
port(
	clk : in std_logic;
	rst : in std_logic;
	ce : in std_logic;
	instruction : out std_logic_vector(31 downto 0);
	PC : out std_logic_vector(31 downto 0);
	PCPlus4 : out std_logic_vector(31 downto 0);
	selNxtPC : in std_logic;
	brAdd : in std_logic_vector(31 downto 0)
);
end component RISCV_IF; 
component RISCV_IM is
port(
	PC : in std_logic_vector(31 downto 0);
	instruction : out std_logic_vector(31 downto 0)
);
end component RISCV_IM; 
component RISCV_EX is
port(
	rs1D : in std_logic_vector(31 downto 0);
	rs2D : in std_logic_vector(31 downto 0);
	extImm : in std_logic_vector(31 downto 0);
	PC : in std_logic_vector(31 downto 0);
	brAdd : out std_logic_vector(31 downto 0);
	ALUOut : out std_logic_vector(31 downto 0);
	DToM : out std_logic_vector(31 downto 0);
	branch : out std_logic;
	selALUOp : in std_logic_vector(3 downto 0);
	selB : in std_logic;
	selA : in std_logic;
	selBrBaseAdd : in std_logic;
	selDToM : in std_logic_vector(1 downto 0)
);
end component RISCV_EX; 
component RISCV_WB is
port(
	DFrM : in std_logic_vector(31 downto 0);
	selMToWB : in std_logic_vector(2 downto 0);
	selWBDat : in std_logic_vector(1 downto 0);
	WBDat : out std_logic_vector(31 downto 0);
	PCPlus4 : in std_logic_vector(31 downto 0);
	ALUOut : in std_logic_vector(31 downto 0)
);
end component RISCV_WB; 
component RISCV_MEM is
port(
	clk : in std_logic;
	MWr : in std_logic;
	MRd : in std_logic;
	DToM : in std_logic_vector(31 downto 0);
	DFrM : out std_logic_vector(31 downto 0);
	address : in std_logic_vector(31 downto 0);
	ce : in std_logic
);
end component RISCV_MEM; 
component RISCV_ID is
port(
	instruction : in std_logic_vector(31 downto 0);
	WBDat : in std_logic_vector(31 downto 0);
	rs1D : out std_logic_vector(31 downto 0);
	rs2D : out std_logic_vector(31 downto 0);
	selALUOp : out std_logic_vector(3 downto 0);
	selDToM : out std_logic_vector(1 downto 0);
	selNxtPC : out std_logic;
	selMToWB : out std_logic_vector(2 downto 0);
	selWBDat : out std_logic_vector(1 downto 0);
	MWr : out std_logic;
	MRd : out std_logic;
	selA : out std_logic;
	selB : out std_logic;
	selBrBaseAdd : out std_logic;
	ce : in std_logic;
	clk : in std_logic;
	rst : in std_logic;
	extImm : out std_logic_vector(31 downto 0);
	branch : in std_logic
);
end component RISCV_ID; 
component RISCV_DEC is
port(
	instruction : in std_logic_vector(31 downto 0);
	RWr : out std_logic;
	rd : out std_logic_vector(4 downto 0);
	rs1 : out std_logic_vector(4 downto 0);
	rs2 : out std_logic_vector(4 downto 0);
	extImm : out std_logic_vector(31 downto 0);
	selA : out std_logic;
	selB : out std_logic;
	selALUOp : out std_logic_vector(3 downto 0);
	selDToM : out std_logic_vector(1 downto 0);
	selBrBaseAdd : out std_logic;
	selMToWB : out std_logic_vector(2 downto 0);
	MWr : out std_logic;
	MRd : out std_logic;
	selWBDat : out std_logic_vector(1 downto 0);
	selNxtPC : out std_logic;
	branch : in std_logic
);
end component RISCV_DEC; 

end MainPackage;
package body MainPackage is
end MainPackage;

