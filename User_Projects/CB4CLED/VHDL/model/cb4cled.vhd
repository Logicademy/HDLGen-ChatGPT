-- Header Section
-- Component Name : cb4cled
-- Title          : 
-- Description    : 
-- Author(s)      : 
-- Company        : 
-- Email          : 
-- Date           : 13/07/2022


-- Library Section
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Entity Section
entity cb4cled is 
Port(
	CE : in std_logic;
	D : in std_logic_vector(3 downto 0);
	Q : out std_logic_vector(3 downto 0);
	ceo : in std_logic
);
end entity cb4cled;

architecture comb of cb4cled is

-- Internal Signals
signal test1 : std_logic;
signal test2 : std_logic_vector(127 downto 0);


begin

proc1_p: process(CE,D,ceo)
begin
	Q <= D;

	-- Complete the process

end process;

conc1_c: Q <= '1';

end comb;