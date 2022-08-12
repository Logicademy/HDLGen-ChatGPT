-- Header Section
-- Component Name : counter
-- Title          : 32 bit counter
-- Description    : To be Completed
-- Author(s)      : 
-- Company        : 
-- Email          : 
-- Date           : 05/08/2022


-- Library Section
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Entity Section
entity counter is 
Port(
	in1 : in std_logic_vector(3 downto 0);
	out1 : out std_logic_vector(127 downto 0);
	in2 : in std_logic;
	out2 : in std_logic
);
end entity counter;

architecture comb of counter is

-- Internal Signals
signal intSig1 : std_logic;


begin

proc1: process(in1,out2)
begin
	out1 <= in1;
	intSig1 <= '0';

	-- Complete the process

end process;

conc1: out1 <= '1';

end comb;