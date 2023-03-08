-- Header Section
-- Component Name : mux21_1
-- Title          : 2-to-1 mux, 1-bit data

-- Description
-- sel is datapath control signal
-- muxOut = muxIn0 when sel  = 0
-- muxOut = muxIn1 when sel  = 1 

-- Author(s)      : JP Byrne
-- Company        : UG
-- Email          : j.byrne34@nuigalway.ie
-- Date           : 27/11/2022

-- entity signal dictionary
-- sel	datapath control signal
-- muxIn1	datapath 1 input signal
-- muxIn0	datapath 0 input signal
-- muxOut	data out signal

-- internal signal dictionary
-- None

-- library declarations
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;


-- entity declaration
entity mux21_1 is 
Port(
	sel : in std_logic;
	muxIn1 : in std_logic;
	muxIn0 : in std_logic;
	muxOut : out std_logic
);
end entity mux21_1;

architecture Combinational of mux21_1 is
-- Internal signal declarations
-- None

begin

muxOut_p: process(sel,muxIn1,muxIn0)
begin
	-- Complete the process if required
	muxOut <= muxIn1;-- default
	
end process;

end Combinational;