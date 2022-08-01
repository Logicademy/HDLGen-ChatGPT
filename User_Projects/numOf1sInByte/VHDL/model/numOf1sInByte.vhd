-- Header Section
-- Component Name : numOf1sInByte
-- Title          : Register the number of asserted bits in a byte
-- Description    : Registers the number of asserted bits in dIn byte.  
 	--Result is 0 to 8 as std_logic_vector(3:0) signal, i.e, Process NSDecode_p uses a variable VarNSNumOf1sInByte and loop to combinationally generate the number of asserted bits in dIn byte, and generates NSNumOf1sInByte signal. 
 	--Process synch_p registers NSNumOf1sInByte as CSNumOf1sInByte 
-- Author(s)      : Fearghal Morgan
-- Company        : NUI Galway 
-- Email          : fearghal.morgan@nuigalway.ie
-- Date           : 22/07/2022


-- Library Section
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Entity Section
entity numOf1sInByte is 
Port(
	clk : in std_logic;
	rst : in std_logic;
	dIn : in std_logic_vector(7 downto 0);
	CSNumOf1sInByte : out std_logic_vector(3 downto 0)
);
end entity numOf1sInByte;

architecture RTL of numOf1sInByte is

-- Internal Signals
signal NSNumOf1sInByte : std_logic_vector;


begin

synch_p: process(clk,rst)
begin
	NSNumOf1sInByte <= '';

	-- Complete the process

end process;

NSDecode_p: process(dIn)
begin
	NSNumOf1sInByte <= '';

	-- Complete the process

end process;

end RTL;