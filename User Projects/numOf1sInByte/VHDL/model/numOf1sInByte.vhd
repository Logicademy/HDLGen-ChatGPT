-- Header Section
-- Component Name : numOf1sInByte
-- Title          : Register the number of asserted bits in a byte
-- Description    : 
--   Registers the number of asserted bits in dIn byte.  
--   Result is 0 to 8 as std_logic_vector(3:0) signal, i.e, “0000” to “1000”
--   Process NSDecode_p uses a variable VarNSNumOf1sInByte and loop to combinationally generate the number of asserted bits in dIn byte, and generates NSNumOf1sInByte signal. 
--   Process synch_p registers NSNumOf1sInByte as CSNumOf1sInByte 
-- Author(s)      : Fearghal Morgan
-- Company        : NUI Galway 
-- Email          : fearghal.morgan@nuigalway.ie
-- Date           : 22/07/2022

-- added start: can this be automatically added?
-- Signal dictionary
--  entity signals
--	 clk 			 system clock strobe, rising edge active
--	 rst  			 asynchronous, high asserted reset
--	 dIn  			 byte input data
--	 CSNumOf1sInByte registered number of asserted (1) bits in the signal dIn

--  internal signals
--	 NSNumOf1sInByte unregistered number of asserted (1) bits in the signal dIn
-- added end 


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

-- delete one line space here.

begin

synch_p: process(clk,rst)
begin
-- 		CSNumOf1sInByte <= (others => '0');
-- added code start
	if rst = '1' then 
		CSNumOf1sInByte <= (others => '0');
	elsif rising_edge(clk) then
		CSNumOf1sInByte <= NSNumOf1sInByte;
	end if;
-- added code end
end_process;

NSDecode_p: process(dIn)
-- NSNumOf1sInByte <= (others => '0');
-- added code start
variable VarNSNumOf1sInByte : std_logic_vector(3 downto 0); 
begin
	VarNSNumOf1sInByte := (others => '0');
	for i in 0 to 7 loop
		if dIn(i) = '1' then
		  NSNumOf1sInByte <= std_logic_vector( unsigned(NSNumOf1sInByte) + 1 ); 
		end if;
	end loop;
	NSNumOf1sInByte <= VarNSNumOf1sInByte;
-- added code end
end_process;

end RTL;