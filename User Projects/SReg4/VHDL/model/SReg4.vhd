-- Header Section
-- Component Name : SReg4
-- Title          : Cascadable 4-bit shift register with asynchronous reset
-- Description    : Cascadable 4-bit shift register with asynchronous reset
 	--ABC details
-- Author(s)      : F Morgan
-- Company        : NUIG
-- Email          : f.m@n.ie
-- Date           : 25/07/2022


-- Library Section
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Entity Section
entity SReg4 is 
Port(
	clk : in std_logic;
	rst : in std_logic;
	ce : in std_logic;
	left : in std_logic;
	ld : in std_logic;
	ldDat : in std_logic_vector(3 downto 0);
	SReg : out std_logic_vector(3 downto 0);
	ceo : out std_logic
);
end entity SReg4;

architecture RTL of SReg4 is

-- Internal Signals
signal NS : std_logic_vector;
signal CS : std_logic_vector;


begin

stateReg_p: process(clk,rst)
begin
	CS <= NS;

	-- Complete the process

end_process;

NSDecode_p: process(ce,left,ld,ldDat,CS)
begin
	ceo <= ce;
	NS <= CS;

	-- Complete the process

end_process;

genCS_c: SReg <= CS;

end RTL;