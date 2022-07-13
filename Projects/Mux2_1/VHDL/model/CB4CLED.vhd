-- Header Section
-- Component Name : CB4CLED
-- Title          : 4-bit Counter
-- Description    : Counter description
-- Author(s)      : Abishek
-- Company        : NUIG
-- Email          : A.Bupathi1@nuigalway.ie
-- Date           : 13/07/2022


-- Library Section
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Entity Section
entity CB4CLED is 
Port(
	D : in std_logic_vector(3 downto 0);
	Q : out std_logic_vector(3 downto 0);
	UP : in std_logic;
	L : in std_logic;
	CE : in std_logic;
	CEO : out std_logic;
	TC : out std_logic;
	CLR : in std_logic;
	C : in std_logic
);
end entity CB4CLED;

architecture comb of CB4CLED is

-- Internal Signals

begin


end comb;