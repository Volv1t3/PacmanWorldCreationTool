
#!------------------------------------
"""
@Author: Santiago Arellano
@Date: 28th March 2025
@Description: The following file contains information pertaining the data model for the GridCreation tool view, at its
core lies a 16x16 grid managed through a numpy multidimensional array. Within each cell we will have a string representing
the color code the user selected in the main view. In addition, this class will contain serialization methods both to a file
as well as to a text that can be passed to the user's clipboard
"""
from argparse import ArgumentError

#!-------------------------------------
import numpy as np;



class PacmanGrid:
    def __init__(self):
        #? Defining internal parameters
        self.internalGridForUserInformation: np.ndarray = np.full((16, 16), "000",
                                                                  dtype='U4')
        self.pacmanCount: int = 0;
        self.ghostCount: dict[str, int] = {
            'ghostOne': 0,
            'ghostTwo': 0,
            'ghostThree': 0,
            'ghostFour': 0
        };
        self.internalColorDefinitions: dict[str, str] = {
            '#00001F': '001F',  # Borders are now blue!
            '#FFDE59': '6767',  # Pacman remains yellow
            '#E4080A': 'F08A',  # Ghost One stays red
            '#5DE2E7': '1BFE',  # Ghost two is cyan!
            '#EFC3CA':'FDDC',   # Ghost three is pink!
            '#7DDA58':'0F00',   #Ghost four is green!
            '#FFFFFF': 'FFFF',  # Normal PowerUps are  now white!
            '#FE9900': 'F5A0'   # Eat Others PowerUps is now yellow!
        }
        self.hardcodedLocationGrid = np.full((16, 16), "",
                                               dtype='U3')
        #? Lets now define the count grid such that we can store the information of each cell's visits
        self.hardCodedVisitsGrid = np.full((16,16), "", dtype='U8')
        #? Lets now define a list of random numbers in the range of 1 through 4 inclusive stored in a pretty format
        self.hardCodedMovementList: list[str] = []
        self.hardCodedMovementList = [f"DEC {np.random.randint(1, 5)}" for _ in range(100)]
        self.hardCodedMovementList[0] = self.hardCodedMovementList[0].replace("DEC ", "movementListValues, DEC ")
        self.hardCodedMovementList[1:] = [value.replace("DEC ", " "*20 + "DEC ") for value in self.hardCodedMovementList[1:]]
        self.initHardCodedLocationGrid()

    def initHardCodedLocationGrid(self) -> None:
        """
        The following method is reponsible for initializing the hardcoded location grid, this grid will be used to store the memory locations that 
        map to MARIEs specific visual memory locations, i.e., from 0xF000 to 0XFFF, and store them in a similar fashion to the grid that is stored 
        for the colors in the grid. The use of this grid is to map pacman locations to actual memory location, whilst colors to not need exact memory locations
        pacman, ghosts, and powerups do require this.
        """
        initial_location: list[chr] = ['F','O','O']
        for row in range(0,16):
            for column in range(0,16):
                if row < 10 and column < 10:
                    initial_location[1] = str(row)
                    initial_location[2] = str(column)
                    self.hardcodedLocationGrid[row][column] = ''.join(initial_location)
                elif row < 10 and column >= 10:
                    initial_location[1] = str(row)
                    initial_location[2] = hex(column)[2:].upper()
                    self.hardcodedLocationGrid[row][column] = ''.join(initial_location)
                elif row >= 10 and column < 10:
                    initial_location[1] = hex(row)[2:].upper()
                    initial_location[2] = str(column)
                    self.hardcodedLocationGrid[row][column] = ''.join(initial_location)
                else:
                    initial_location[1] = hex(row)[2:].upper()
                    initial_location[2] = hex(column)[2:].upper()
                    self.hardcodedLocationGrid[row][column] = ''.join(initial_location)
        print(self.hardcodedLocationGrid)
    def setValueOnGridCell(self, gridX: int, gridY: int, color: str) -> bool:
        """
        This method allows the upper level view to add a value into a single cell, the idea of this method is to be called
        right after one cell is clicked in the UI, allowing the operation to be handled directly.
        :param gridX X coordinate passed as the row
        :param gridY Y coordinate passed as the column
        :param color Color string to be stored in the array
        :return bool flag indicating success or failure in the operation
        """
        if self.internalGridForUserInformation[gridX][gridY]:
            self.clearValueFromGridCell(gridX, gridY)
        if color in self.internalColorDefinitions.keys():
            if color == '#FFDE59': #Pacman Color
                pacmanCount = self.get_pacman_count()
                if pacmanCount == 0:
                    self.increment_pacman_count_by_one()
                    self.internalGridForUserInformation[gridX][gridY] \
                        = self.internalColorDefinitions.get(color)
                    return True
                else:
                    return False
            elif color == "#E4080A": #Ghost One Color
                ghostCount: int = self.get_ghost_count('ghostOne')
                if ghostCount < 1:
                    self.increment_ghost_count_by_one('ghostOne')
                    self.internalGridForUserInformation[gridX][gridY] = \
                        self.internalColorDefinitions.get(color)
                    return True
                else:
                    return False
            elif color == "#5DE2E7": #Ghost Two COlor
                ghostCount: int = self.get_ghost_count('ghostTwo')
                if ghostCount < 1:
                    self.increment_ghost_count_by_one('ghostTwo')
                    self.internalGridForUserInformation[gridX][gridY] = \
                        self.internalColorDefinitions.get(color)
                    return True
                else:
                    return False
            elif color == "#EFC3CA": #Ghost Three Color
                ghostCount: int = self.get_ghost_count('ghostThree')
                if ghostCount < 1:
                    self.increment_ghost_count_by_one('ghostThree')
                    self.internalGridForUserInformation[gridX][gridY] = \
                        self.internalColorDefinitions.get(color)
                    return True
                else:
                    return False
            elif color == "#7DDA58": #? Ghost Four Color
                ghostCount: int = self.get_ghost_count('ghostFour')
                if ghostCount < 1:
                    self.increment_ghost_count_by_one('ghostFour')
                    self.internalGridForUserInformation[gridX][gridY] = \
                        self.internalColorDefinitions.get(color)
                    return True
                else:
                    return False
            else:
                self.internalGridForUserInformation[gridX][gridY] = \
                    self.internalColorDefinitions.get(color)
                return True
        else:
            return False
    def clearValueFromGridCell(self, gridX: int, gridY: int) -> bool:
        """
        This method allows the upper level view to clear a value from a single cell, the idea of this method is to be called
        from the UI using a button or an eraser tool, what it will do its inform both the UI and the subsystem of a color
        decision being revered
        :param gridX: X coordinate passed as the row
        :param gridY: Y coordinate passed as the column
        """
        gridValue: str = self.internalGridForUserInformation[gridX][gridY].item()
        if gridValue == self.internalColorDefinitions.get("#FFDE59"):
            self.decrement_pacman_count_by_one()
            self.internalGridForUserInformation[gridX][gridY] = "000"
            return True
        elif gridValue == self.internalColorDefinitions.get("#E4080A"):
            self.decrement_ghost_count_by_one('ghostOne')
            self.internalGridForUserInformation[gridX][gridY] = "000"
            return True
        elif gridValue == self.internalColorDefinitions.get("#5DE2E7"):
            self.decrement_ghost_count_by_one('ghostTwo')
            self.internalGridForUserInformation[gridX][gridY] = "000"
            return True
        elif gridValue == self.internalColorDefinitions.get("#EFC3CA"):
            self.decrement_ghost_count_by_one('ghostThree')
            self.internalGridForUserInformation[gridX][gridY] = "000"
            return True
        elif gridValue == self.internalColorDefinitions.get("#7DDA58"):
            self.decrement_ghost_count_by_one('ghostFour')
            self.internalGridForUserInformation[gridX][gridY] = "000"
            return True
        else:
            self.internalGridForUserInformation[gridX][gridY] = "000"
            return True

    def __str__(self) -> str:
        """
        This method is responsible for serializing the internal grid into a string that can be written to a file or to the
        user's clipboard
        :return: A string that can be written to a file or to the user's clipboard
        """
        #?---------------------------
        # In order to make this method work, the serialization is adapted only for my idea of the project, the implementation details here
        # can be changed to suite your own needs, but for me what I need is specific: 1) An array of the memory locations, beginning at 0xF000
        # and holding all locations of pacman and the ghosts, as well as the locations of powerups. 2) A series of lists  that represent the colors 
        # that have been stored per row in the grid. The idea is to serialize 16 lists that represent the 16 rows of the grid, each list holding 16 
        # elements represented by the colors I have defined in the internalColorDefinitions dictionary.
        #?--------------------------
        #! 1. Creating the array of pacman, ghost, and powerups locations
        serializable_result: str = ""
        pacman_location: str = ""
        ghost_locations: list[str] = []
        normal_powerups_locations: list[str] = []
        eat_others_powerups_locations: list[str] = []
        for row in range(0, 16):
            for column in range(0, 16):
                cell_value = self.internalGridForUserInformation[row][column]
                location = self.hardcodedLocationGrid[row][column]
                if cell_value == self.internalColorDefinitions.get("#FFDE59"):  # Pacman creation
                    pacman_location = f"pacmanEntityArray, HEX {location}"
                elif cell_value == self.internalColorDefinitions.get("#E4080A"):  # Ghost One
                    ghost_locations.append(f"redGhostOriginalLocation, HEX {location}")
                elif cell_value == self.internalColorDefinitions.get("#5DE2E7"):  # Ghost Two
                    ghost_locations.append(f"cyanGhostOriginalLocation, HEX {location}")
                elif cell_value == self.internalColorDefinitions.get("#EFC3CA"):  # Ghost Three
                    ghost_locations.append(f"pinkGhostOriginalLocation, HEX {location}")
                elif cell_value == self.internalColorDefinitions.get("#7DDA58"):  # Ghost Four
                    ghost_locations.append(f"greenGhostOriginalLocation, HEX {location}")
                elif cell_value in [self.internalColorDefinitions.get("#FFFFFF")]:  # PowerUps creation
                    normal_powerups_locations.append(f"normalPowerUpsLocations, HEX {location}")
                elif cell_value in [self.internalColorDefinitions.get("#FE9900")]:
                    eat_others_powerups_locations.append(f"eatOthersPowerUpsLocations, HEX {location}")
        serializable_result += pacman_location
        ghost_locations[1:] = [entry.replace("ghostEntityArray,"," "*20) for entry in ghost_locations[1:]]
        normal_powerups_locations[1:] = [entry.replace("normalPowerUpsLocations,"," "*20) for entry in normal_powerups_locations[1:]]
        eat_others_powerups_locations[1:] = [entry.replace("eatOthersPowerUpsLocations, ", " "*20) for entry in eat_others_powerups_locations[1:]]
        serializable_result += "\n" + "\n".join(ghost_locations)
        serializable_result += "\n" + "\n".join(normal_powerups_locations)
        serializable_result += "\n" + "\n".join(eat_others_powerups_locations)

        #! 2. Creating the array of colors for each row within the internal structure
        per_row_color_location: list[str] = []

        for row in range(0,16):
            row_locations: list[str] = []
            for column in range(0,16):
                row_locations.append("colorLocationArrayForRow, " + "HEX " +self.internalGridForUserInformation[row][column])
            #? Now lets reorder it such that only the first location has the MARIE heading style
            if row == 0:
                row_locations[1:] = [entry.replace("colorLocationArrayForRow,"," "*20) for entry in row_locations[1:]]
            else:
                row_locations[:] = [entry.replace("colorLocationArrayForRow,"," "*20) for entry in row_locations[:]]
            per_row_color_location.append("\n".join(row_locations))
        
        #! 3. Lets add the serialiazed rows into the final result string
        serializable_result += "\n" + "\n".join(per_row_color_location)

        #! 4. Lets add the movement grid to the output
        serializable_result += "\n" + "\n".join(self.hardCodedMovementList)

        return serializable_result
    
    
    def get_pacman_count(self) -> int:
        return self.pacmanCount;
    def get_ghost_count(self, ghostType: str) -> int:
        return self.ghostCount.get(ghostType);
    def increment_pacman_count_by_one(self) -> None:
        self.pacmanCount +=1;
    def increment_ghost_count_by_one(self, ghostType: str)-> None:
        self.ghostCount[ghostType] +=1;
    def decrement_pacman_count_by_one(self) -> None:
        if self.pacmanCount > 0:
            self.pacmanCount -=1;
        elif self.pacmanCount == 0:
            self.pacmanCount = 0
    def decrement_ghost_count_by_one(self, ghostType: str) -> None:
        if self.ghostCount.get(ghostType) > 0:
            self.ghostCount[ghostType] -=1;
        elif self.ghostCount.get(ghostType) == 0:
            self.ghostCount[ghostType] = 0