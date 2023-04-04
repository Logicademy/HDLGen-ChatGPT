-- Header Section
-- Component Name : memorySys
-- Title          : 2 x 4-digit memory array write/read and bank select mux

-- Description
-- System contains 2 x synchronous write / combinational read register memory arrays (4 x 4-bit arrays)
-- ce enable all registers
-- selMemBankToBeWritten selects register array memory bank select for writes
-- we assertion enables synchronous writes
-- Write data is dIn(3:00)
-- selMemBankToBeRead selects register array memory bank select for reads, with output data dOut(3:0)

-- Author(s)      : Fearghal Morgan
-- Company        : University of Galway
-- Email          : fearghal.morgan@universityofgalway.ie
-- Date           : 02/04/2023

-- entity signal dictionary
-- clk	clk signal
-- rst	rst signal
-- selMemBankToBeWritten	select memory array to be written to
-- we	Synchronous write enable
-- add	memory address
-- dIn	4-bit input data bus
-- dOut	4-bit data output
-- ce	Chip enable
-- selMemBankToBeRead	0 select reg4x4() memory output data, 1 select reg4x4() 
-- memory output data

-- internal signal dictionary
-- dOut_1	memory back 1 data array
-- dOut_0	memory back 0 data array
-- selCe1	selCe1 = ce and selMemBankToBeWritten
-- selCe0	selCe0 = ce and (not selMemBankToBeWritten)

-- library declarations
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.MainPackage.all;

-- entity declaration
entity memorySys is 
Port(
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
end entity memorySys;

architecture RTL of memorySys is
-- Internal signal declarations
signal dOut_1 : std_logic_vector(3 downto 0);
signal dOut_0 : std_logic_vector(3 downto 0);
signal selCe1 : std_logic;
signal selCe0 : std_logic;

begin

mux21_4_i: mux21_4 -- Complete the concurrent statement if required
port map(
	mux21_4_In1 => dOut_1,
	mux21_4_In0 => dOut_0,
	sel => selMemBankToBeRead,
	mux21_4_Out => dOut
	);

reg4x4_1_i: reg4x4 -- Complete the concurrent statement if required
port map(
	clk => clk,
	rst => rst,
	ce => selCe1,
	we => we,
	add => add,
	dIn => dIn,
	dOut => dOut_1
	);

reg4x4_0_i: reg4x4 -- Complete the concurrent statement if required
port map(
	clk => clk,
	rst => rst,
	ce => selCe0,
	we => we,
	add => add,
	dIn => dIn,
	dOut => dOut_0
	);
selCe0_c: selCe0 <= ce and (not selMemBankToBeWritten); -- Complete the concurrent statement if required

selCe1_c: selCe1 <= ce and selMemBankToBeWritten; -- Complete the concurrent statement if required

end RTL;