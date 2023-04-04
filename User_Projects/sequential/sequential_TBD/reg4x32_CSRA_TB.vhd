-- Description: reg4x32_CSRA_TB testbench 
-- Engineer: Fearghal Morgan
-- National University of Ireland, Galway / viciLogic 
-- Date: 30/10/2019

-- Refer to reg4x32_CSRA VHDL model for component specification and signal descriptions

-- Change History: Initial version

-- Reference: https://tinyurl.com/vicilogicVHDLTips   	A: VHDL IEEE library source code VHDL code
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.numeric_std.all;
use work.arrayPackage.all;

entity reg4x32_CSRA_TB is end reg4x32_CSRA_TB; -- testbench has no inputs or outputs

architecture Behavioral of reg4x32_CSRA_TB is
-- component declaration is in package

-- Declare internal testbench signals, typically the same as the component entity signals
-- initialise signal clk to logic '1' since the default std_logic type signal state is 'U' 
-- and process clkStim uses clk <= not clk  
signal clk       : STD_LOGIC := '1'; 
signal rst       : STD_LOGIC;
signal clr00     : std_logic;
signal ld0       : std_logic;

signal we        : std_logic;
signal add       : std_logic_vector( 1 downto 0);					 
signal dIn       : std_logic_vector(31 downto 0);
signal reg       : array4x32;
signal dOut      : std_logic_vector(31 downto 0);

signal reg4x32_CSRA_arrayA : array4x32; 

constant period   : time := 20 ns;    -- 50MHz clk
signal   endOfSim : boolean := false; -- Default FALSE. Assigned TRUE at end of process stim
signal   testNo   : integer;          -- facilitates test numbers. Aids locating each simulation waveform test 

begin

uut: reg4x32_CSRA_c -- instantiate unit under test (UUT)
port map ( clk       => clk,       		  
           rst       => rst, 
		   clr00     => clr00,
		   ld0       => ld0,

		   we	     => we,
		   add       => add,  
		   dIn       => dIn,
		   
		   reg       => reg, 
           dOut      => dOut
         );

-- clk stimulus continuing until all simulation stimulus have been applied (endOfSim TRUE)
clkStim : process (clk)
begin
  if endOfSim = false then
     clk <= not clk after period/2;
  end if;
end process;

stim: process -- no process sensitivity list to enable automatic process execution in the simulator
variable varReg4x32_CSRA_arrayA : array4x32; 
begin 
  report "%N : Simulation Start."; -- generate messages as the simulation executes 
  -- initialise all input signals 

  clr00     <= '0';  -- defaults
  ld0       <= '0';  
  we        <= '0';   
  add       <= (others => '0'); 
  dIn       <= (others => '0');
  
  testNo <= 0; -- include a unique test number to help browsing of the simulation waveform     
  -- apply rst signal pattern, to deassert 0.2*period after the active clk edge
  -- verify that register(3) is correctly initialised on rst assertion
  rst <= '1';
  wait for 1.2 * period;
  rst <= '0';
  -- wait for period;  

  testNo  <= 1; -- write to all registers
  varReg4x32_CSRA_arrayA := reg4x32_CSRA_arrayA;
  we      <= '1';
  dIn <= X"00000000"; -- default 
  for i in 0 to 3 loop -- write 0x5A5A5A5A to all registers. 
    add   <= std_logic_vector( to_unsigned(i,2) );
    dIn <= varReg4x32_CSRA_arrayA(i); 
    wait for period;  
  end loop;

  testNo  <= 2;       -- read all registers
  we      <= '0';
  dIn     <= (others => '0'); 
  for i in 0 to 3 loop
    add   <= std_logic_vector( to_unsigned(i,2) );
    wait for period;  
  end loop;
  we      <= '0';  

  testNo  <= 3;     -- assert clr00. Should clear array register(0)(0) 
  clr00     <= '1'; 
  wait for period;  
  clr00     <= '0'; 

  testNo  <= 4;     -- assert ld0. Should clear all array register bits 
  ld0     <= '1'; 
  wait for period;  
  ld0     <= '0'; 


  ld0       <= '0';  -- default values
  we        <= '0';   
  add       <= (others => '0'); 
  dIn       <= (others => '0');
  wait for period;  

  endOfSim <= true;   		 -- assert flag. Stops clk signal generation in process clkStim
  report "simulation done";   
  wait; 					 -- include to prevent the stim process from repeating execution, since it does not include a sensitivity list
  
end process;

  
reg4x32_CSRA_arrayA <= 
     (0     => X"deadbeef",      
      1     => X"c001cafe",      
      2     => X"c001100c",      
     others => X"f00dcafe"   
  );


end Behavioral;