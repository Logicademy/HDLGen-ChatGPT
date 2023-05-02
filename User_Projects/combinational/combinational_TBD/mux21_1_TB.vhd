--  mux21_1_TB testbench 
--  Author(s)		Fearghal Morgan
--  Company			National University of Ireland, Galway 
--  Date			6th Dec 2021
--  Change History 	Initial version

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity mux21_1_TB is end mux21_1_TB;

architecture behave of mux21_1_TB is

component mux21_1
    port (sel    : in std_logic;
          muxIn1 : in std_logic;
          muxIn0 : in std_logic;
          muxOut : out std_logic);
end component;

signal sel    : std_logic;
signal muxIn1 : std_logic;
signal muxIn0 : std_logic;
signal muxOut : std_logic;

signal testNo   : integer;          -- Aids locating test in simulation waveform 
signal endOfSim : boolean := false; -- assert at end of simulation 

begin

uut : mux21_1 -- unit under test
port map (sel    => sel,
          muxIn1 => muxIn1,
          muxIn0 => muxIn0,
          muxOut => muxOut);

stim_i: process -- Stimulus process
variable tempVec : std_logic_vector(2 downto 0); -- variable changes immediately on assignment (using := operator)
                                                 -- Can use variable to define stimulus signal sequence 
begin
    report "%N : Simulation start";
	sel    <= '0';  -- default input signal values
	muxIn1 <= '0';  
	muxIn0 <= '0';  
    endOfSim <= false;

    testNo <= 0;    -- including variable/signal loop for reference
    for i in 0 to 7 loop
	  tempVec := std_logic_vector(TO_UNSIGNED(i, 3)); -- generate 3-bit vector
      wait for 10 ns;  
    end loop; 

    testNo <= 1;
	sel    <= '0';  
	muxIn1 <= '0';  
	muxIn0 <= '0';  
    wait for 10 ns; 

    endOfSim <= true;
    report "%N : Simulation end";

	wait;
	
end process;

END behave;