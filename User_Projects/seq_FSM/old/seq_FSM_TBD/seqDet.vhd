-- Model name: seqDet
-- Description: sequence detector 
-- Authors: Fearghal Morgan, National University of Ireland, Galway 
-- Date: 27/7/2018
-- For viciLogic projects, use FPGA Zynq technology part XC7Z020CLG400-1 (for Digilent PYNQ-Z1 module)
-- 
-- Signal data dictionary
--  clk             input   System clock strobe
--  rst             input   Asynchronous clear. Assertion (h) clears all registers  
--  userCode(1:0)   input   Entered code value. Valid sequence defined in specification (flowchart) 
--  validCode   	input	Assertion (h) validates code(1:0) entry
--  openLock		output  Asserted when CS(1:0) = "11"
--
-- Incremental signal data dictionary
--  CS(1:0)			input	Current state, registered NS
--  NS(1:0)			output  Next state. Logic is described in specification(flowchart and NS(1:0) function table)

-- use default libraries
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity seqDet is
    Port (clk       : in  std_logic;
          rst       : in  std_logic; 
 	      userCode  : in  STD_LOGIC_VECTOR(1 downto 0);  
          validCode : in  STD_LOGIC;    
          openLock  : out STD_LOGIC   
          );
end seqDet;

architecture RTL of seqDet is
-- Declare enumerated types for CS and NS state signals
-- The synthesis tool will select the encoding of CS and NS 
-- (binary, gray, one-hot, random 
type stateType is (getCode0, getCode1, getCode2, codeDetected); 
signal CS, NS: stateType;  -- current and next state signals
begin

stateReg: process (clk, rst)
begin
    if rst = '1' then 
        CS <= getCode0;
    elsif rising_edge(clk) then
        CS <= NS;
    end if;
end process;

-- Describing case/if statements with enumerated state type
NSDecode: process (CS, userCode, validCode)
begin
    NS <= CS; -- default assignment. Covers all 'stay in state' assignment
	openLock <= '0';
	case CS is	
		when getCode0     => if userCode="10" and validCode='1' then NS <= getCode1; end if;
		when getCode1     => if userCode="11" and validCode='1' then NS <= getCode2; end if;
		when getCode2     => if userCode="01" and validCode='1' then NS <= codeDetected; end if;
		when codeDetected => openLock <= '1';
		when others   => null;
    end case;
end process;

end RTL;





-- -- Describing case/if statements with enumerated state type
-- NSDecode: process (CS, userCode, validCode)
-- begin
    -- NS <= CS; -- default assignment. 
	-- openLock <= '0';
	-- case CS is	
		-- when getCode0 => 
			-- if userCode="10" and validCode='1' then 
				-- NS <= getCode1; 
			-- end if;
		-- when getCode1 => 
			-- if userCode="11" and validCode='1' then 
				-- NS <= getCode2; 
			-- end if;
		-- when getCode2 => 
			-- if userCode="01" and validCode='1' then 
				-- NS <= codeDetected; 
			-- end if;
		-- when codeDetected => 
			-- openLock <= '1';
		-- when others   => null;
    -- end case;
-- end process;






-- -- Describing case/if statements with enumerated state type
-- NSDecode: process (CS, userCode, validCode)
-- begin
    -- NS <= CS; -- default assignment. Covers all 'stay in state' assignment
	-- case CS is	
		-- when getCode0 => if userCode="10" and validCode='1' then NS <= getCode1; end if;
		-- when getCode1 => if userCode="11" and validCode='1' then NS <= getCode2; end if;
		-- when getCode2 => if userCode="01" and validCode='1' then NS <= codeDetected; end if;
		-- -- don't need to include when codeDetected since NS <= CS applies in this state, and already in default
		-- when others   => null;
    -- end case;
-- end process;

-- -- Describing case/if statements with enumerated state type
-- NSDecode: process (CS, userCode, validCode)
-- begin
    -- NS <= CS; -- default assignment. 
	-- case CS is	
		-- when getCode0 => 
			-- if userCode="10" and validCode='1' then 
				-- NS <= getCode1; 
			-- end if;
		-- when getCode1 => 
			-- if userCode="11" and validCode='1' then 
				-- NS <= getCode2; 
			-- end if;
		-- when getCode2 => 
			-- if userCode="01" and validCode='1' then 
				-- NS <= codeDetected; 
			-- end if;
		-- when others   => null;
    -- end case;
-- end process;


-- OPDecode: process (CS)
-- begin
    -- openLock <= '0'; -- default. 
    -- if CS = "11" then 
        -- openLock <= '1';
    -- end if;        
-- end process;








-- signal CS : STD_LOGIC_VECTOR(1 downto 0);  
-- signal NS : STD_LOGIC_VECTOR(1 downto 0);  
-- NSDecode: process (CS, userCode, validCode)
-- begin
	-- NS <= CS; -- default
    -- if validCode='1' then 
	  -- case CS is	
		-- when "00" => if userCode="10" then NS <= "01"; end if;
		-- when "01" => if userCode="11" then NS <= "10"; end if;
		-- when "10" => if userCode="01" then NS <= "11"; end if;
		-- when others => null;
      -- end case;
    -- end if;
-- end process;




-- describing case/if statements using separate lines and indenting
-- NSDecode: process (CS, userCode, validCode)
-- begin
	-- NS <= CS; -- default
    -- case CS is	
		-- when "00"   => 
			-- if userCode="10" and validCode='1' then 
				-- NS <= "01"; 
			-- end if;
		-- when "01"   => 
			-- if userCode="11" and validCode='1' then 
				-- NS <= "10"; 
			-- end if;
		-- when "10"   => 
			-- if userCode="01" and validCode='1' then 
				-- NS <= "11"; 
			-- end if;
		-- when others => 
			-- null;
    -- end case;
-- end process;

-- -- Inefficient: long-winded process, describing every path and signal state assignments
-- NSDecode: process (CS, userCode, validCode)
-- begin
    -- case CS is	
		-- when "00"   => 
			-- if validCode='0' then 
					-- NS <= "00";      -- NS<=CS 
					-- openLock <= '0'; -- default value
			-- else                     -- do not need to state the obvious, i.e, elsif validCode='1' then 
				-- if userCode="10" then 
					-- NS <= "01"; 
					-- openLock <= '0'; -- default value
				-- else
					-- NS <= "00";      -- NS<=CS 
					-- openLock <= '0'; -- default value
				-- end if;
			-- end if;

		-- when "01"   => 
			-- if validCode='0' then 
					-- NS <= "01";      -- NS<=CS 
					-- openLock <= '0'; -- default value
			-- else                     -- do not need to state the obvious, i.e, elsif validCode='1' then 
				-- if userCode="11" then 
					-- NS <= "10"; 
					-- openLock <= '0'; -- default value
				-- else
					-- NS <= "01";      -- NS<=CS 
					-- openLock <= '0'; -- default value
				-- end if;
			-- end if;
			
		-- when "10"   => 
			-- if validCode='0' then 
					-- NS <= "10";      -- NS<=CS 
					-- openLock <= '0'; -- default value
			-- else                     -- do not need to state the obvious, i.e, elsif validCode='1' then 
				-- if userCode="01" then 
					-- NS <= "11"; 
					-- openLock <= '0'; -- default value
				-- else
					-- NS <= "10";      -- NS<=CS 
					-- openLock <= '0'; -- default value
				-- end if;
			-- end if;
			
		-- when "11" => 
			-- NS <= "11";              -- NS<=CS 
			-- openLock <= '0';         -- default value

		-- when others => 				 -- this CS(1:0) input state should not occur, since all 4 states described
			-- NS <= "00";              -- select arbitrary value
			-- openLock <= '0';         -- default value
		-- null;
    -- end case;
-- end process;





-- NSDecode: process (CS, userCode, validCode)
-- begin
	-- NS <= CS; -- default
    -- case CS is	
		-- when "00"   => if userCode="10" and validCode='1' then NS <= "01"; end if;
		-- when "01"   => if userCode="11" and validCode='1' then NS <= "10"; end if;
		-- when "10"   => if userCode="01" and validCode='1' then NS <= "11"; end if;
		-- when others => null;
    -- end case;
-- end process;


-- -- Using enumerated types for CS and NS state signals
-- -- The synthesis tool will select the encoding of CS and NS (binary, gray, one-hot, random 
-- type stateType is (getCode0, getCode1, getCode2, codeDetected); -- declare enumerated state type
-- signal CS, NS: stateType;  -- current and next state signals

-- NSDecode: process (CS, userCode, validCode)
-- begin
	-- NS <= CS; -- default. Assignment covers all 'remain in state' logic 
    -- case CS is	
		-- when getCode0 => if userCode="10" and validCode='1' then NS <= getCode1; end if;
		-- when getCode1 => if userCode="11" and validCode='1' then NS <= getCode2; end if;
		-- when getCode2 => if userCode="01" and validCode='1' then NS <= codeDetected; end if;
		-- when others   => null;
    -- end case;
-- end process;


-- describing case/if statements using separate lines and indenting, with enumerated state type
-- NSDecode: process (CS, userCode, validCode)
-- begin
    -- case CS is	
		-- when getCode0 => 
			-- if userCode="10" and validCode='1' then 
				-- NS <= getCode1; 
			-- end if;
		-- when getCode1 => 
			-- if userCode="11" and validCode='1' then 
				-- NS <= getCode2; 
			-- end if;
		-- when getCode2 => 
			-- if userCode="01" and validCode='1' then 
				-- NS <= codeDetected; 
			-- end if;
		-- when others   => null;
    -- end case;
-- end process;





-- -- describing case/if statements using separate lines and indenting
-- NSDecode: process (CS, userCode, validCode)
-- begin
	-- NS <= CS; -- default. Assignment covers all 'remain in state' logic 
    -- case CS is	
		-- when getCode0 => 
			-- if userCode="10" and validCode='1' then 
				-- NS <= getCode1; 
			-- end if;
		-- when getCode1 => 
			-- if userCode="11" and validCode='1' then 
				-- NS <= getCode2; 
			-- end if;
		-- when getCode2 => 
			-- if userCode="01" and validCode='1' then 
				-- NS <= codeDetected; 
			-- end if;
		-- when others   => null;
    -- end case;
-- end process;


