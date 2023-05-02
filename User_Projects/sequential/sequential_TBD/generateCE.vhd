-- generateCE VHDL model 
-- Engineer: Fearghal Morgan, National University of Ireland, Galway
-- Date: Sept 2022

-- Description
-- generates function control signal ce, for single stepping or running at speed

-- Signal dictionary
--   clk
--   rst
--   enSingleStep 
--     if enSingleStep = '0', ce = '1' 
--     if enSingleStep = '1', assert signal step to assert ce for one clk period, deassert signal step before reasserting 
--   ce signal controls operation of DSP functions

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use work.arrayPackage.all;

entity generateCE is 
    Port (clk  	           : in  STD_LOGIC;
          rst              : in  STD_LOGIC;		  
          enSingleStep     : in  std_logic;
          step             : in  std_logic;
		  ce               : out std_logic
          );	
end generateCE;

architecture RTL of generateCE is
type stateType is (waitFor1, waitFor0); -- declare enumerated state type
signal CS, NS : stateType;     			-- declare state signals 
signal stepPulse : std_logic;

begin

--genStepPulse_i: singleShot 
--Port map (clk   => clk, 
--          rst   => rst,  
--          sw    => step,
--          aShot	=> stepPulse
--	  ); 
    
-- Synchronous process defining state value
stateReg_i: process (clk, rst)
begin
  if rst = '1' then 		
    CS <= waitFor1;		
  elsif clk'event and clk = '1' then 
    CS <= NS;
  end if;
end process; 

-- Next state and o/p decode process
NSAndOPDec_i: process (CS, step)
begin
   stepPulse <= '0';    				-- default assignment of process o/p signals 
   NS 	     <= CS; 				
   
   case CS is
		when waitFor1 => 			-- move to state waitFor0 if sw = '1'. 
									-- Otherwise no change from default values
			if step = '1' then 
				stepPulse <= '1';    	-- combinationally assert unregistered o/p
				NS <= waitFor0;
			end if;
		when waitFor0 => 			-- remain in state waitFor0 unless sw = '0'. 
								    -- Otherwise no change from default values
			if step = '0' then 
				NS <= waitFor1;
			end if;
		when others => 
			null;           		-- do nothing since default assignments apply
   end case;
end process; 

genCE_i: process(enSingleStep, stepPulse) 
begin
  ce <= '1';
  if enSingleStep = '1' then
	ce <= stepPulse;
  end if;
end process;

end RTL;