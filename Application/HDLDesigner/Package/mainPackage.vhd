-- Package
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
package arrayPackage is
type reg4x4_Array is array(4 downto 0) of std_logic_vector(4 downto 0);
type reg4x32_Array is array(4 downto 0) of std_logic_vector(32 downto 0);
type reg32x32_Array is array(32 downto 0) of std_logic_vector(32 downto 0);

component mux21_4 is
port(
	mux21_4_In1 : in std_logic_vector(3 downto 0);
	mux21_4_In0 : in std_logic_vector(3 downto 0);
	sel : in std_logic;
	mux21_4_Out : out std_logic_vector(3 downto 0)
);
end component mux21_4; 
component reg4x4 is
port(
	clk : in std_logic;
	rst : in std_logic;
	ce : in std_logic;
	we : in std_logic;
	add : in std_logic_vector(1 downto 0);
	dIn : in std_logic_vector(3 downto 0);
	dOut : out std_logic_vector(3 downto 0)
);
end component reg4x4; 
component mux21_1 is
port(
	sel : in std_logic;
	muxIn1 : in std_logic;
	muxIn0 : in std_logic;
	muxOut : out std_logic
);
end component mux21_1; 
component CB4CLED is
port(
	load : in std_logic;
	loadDat : in std_logic_vector(3 downto 0);
	ce : in std_logic;
	up : in std_logic;
	count : out std_logic_vector(3 downto 0);
	TC : out std_logic;
	ceo : out std_logic;
	clk : in std_logic;
	rst : in std_logic
);
end component CB4CLED; 
component ADD2 is
port(
	addIn1 : in std_logic_vector(1 downto 0);
	addIn0 : in std_logic_vector(1 downto 0);
	sum : out std_logic_vector(1 downto 0)
);
end component ADD2; 
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

end arrayPackage;
package body arrayPackage is
end arrayPackage;

