import pygame
import sys
import UI
import PlaceComponent
import numpy

# Initialize Pygame
pygame.init()

# Set up display
window_width, window_height = 1280, 720
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Circuit Simulator")

# Define colors
LINECOLOUR = (130, 130, 130)
BACKGROUND = (200, 200, 200)
BLACK = (0, 0, 0)

# Define camera position and zoom
zoom = -1.7
zoomChange = 0.1
gridLength = 1
xPos = 0 # Both relative to center of screem
#xPos on screen is {xPos * pow(0.1, zoom) + window_width/2}
yPos = 0
PrevXPos = 0
PrevYPos = 0
storeMouseX = 0
storeMouseY = 0

# Move camera center
buttonPressedBefore = 0

# handle buttons clicked
placementState = 0

# Draw wires
circleSize = 10


#convert from the original grid to screen coordinates
def gridToScreenX(coordinate):
    return (window_width/2 + pow(0.1, zoom) * (xPos + coordinate))

def gridToScreenY(coordinate):
    return (window_height/2 + pow(0.1, zoom) * (yPos + coordinate))


def screenToGridX(coordinate):
    return ((coordinate - window_width/2 - xPos * pow(0.1, zoom)) / pow(0.1, zoom))

def screenToGridY(coordinate):
    return ((coordinate - window_height/2 - yPos * pow(0.1, zoom)) / pow(0.1, zoom))

#Handle placement and button use
class state:
    liveSimulation = 0
    placingComponents = 0
    component = None


globalState = state()

#Handle button use
buttons = [UI.wireButton, UI.voltage_sourceButton, UI.resistorButton, UI.capacitorButton, UI.inductorButton, UI.startStopButton]
buttonPressedBefore = 0  # State to check if a button was pressed before

# Map each component-placement button to the component name it places.
# Used to replace a long chain of near-identical if/elif blocks below.
componentButtonMap = {
    UI.wireButton:           "wire",
    UI.voltage_sourceButton: "voltage_source",
    UI.resistorButton:       "resistor",
    UI.capacitorButton:      "capacitor",
    UI.inductorButton:       "inductor",
}

################################################################################################


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                buttonPressedBefore = 1  # Set button pressed state after clicking a button
                for b in buttons:
                    if b.isClicked(mouse_x, mouse_y, window_width, window_height):

                        buttonPressedBefore = 0  # Reset button pressed state after clicking a button
                        
                        globalState.placingComponents = 0  # Reset component placement state

                        # Handle button clicks
                        if b == UI.startStopButton:
                            globalState.liveSimulation = not globalState.liveSimulation
                        elif b in componentButtonMap:
                            componentName = componentButtonMap[b]
                            if globalState.component == componentName:
                                # Clicking the already-selected button deselects it
                                placementState = 0
                                globalState.component = None
                            else:
                                # Otherwise select this component for placement
                                placementState = 1
                                globalState.component = componentName


    
                # Handle placement of components
                if placementState == 1 and buttonPressedBefore == 1:

                    if globalState.placingComponents == 0:
                        globalState.placingComponents = 1

                        # Store the initial position for placement
                        globalState.storeMouseX = round(screenToGridX(mouse_x))
                        globalState.storeMouseY = round(screenToGridY(mouse_y))

                    elif globalState.placingComponents == 1:
                        globalState.placingComponents = 0

                        # Place the component at the stored position.
                        # All component types share the same placement call,
                        # so a single dispatch handles every case.
                        if globalState.component in componentButtonMap.values():
                            PlaceComponent.place_component(
                                globalState.component,
                                globalState.storeMouseX,
                                globalState.storeMouseY,
                                round(screenToGridX(mouse_x)),
                                round(screenToGridY(mouse_y)),
                            )


            if event.button == 4:
                storeMouseX = screenToGridX(mouse_x)
                storeMouseY = screenToGridY(mouse_y)
                zoom += -zoomChange
                xPos += screenToGridX(mouse_x) - storeMouseX
                yPos += screenToGridY(mouse_y) - storeMouseY
            if event.button == 5:
                storeMouseX = screenToGridX(mouse_x)
                storeMouseY = screenToGridY(mouse_y)
                zoom += zoomChange
                xPos += screenToGridX(mouse_x) - storeMouseX
                yPos += screenToGridY(mouse_y) - storeMouseY
                
    if globalState.liveSimulation == True:
        PlaceComponent.extSolve()

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Change center position
    mouse_Pressed = pygame.mouse.get_pressed()
    if mouse_Pressed[2]:
        if buttonPressedBefore:
            xPos += (mouse_x - PrevXPos) * pow(10, zoom)
            yPos += (mouse_y - PrevYPos) * pow(10, zoom)
            PrevXPos = mouse_x
            PrevYPos = mouse_y
        else:
            PrevXPos = mouse_x
            PrevYPos = mouse_y
        buttonPressedBefore = 1
    else:
        buttonPressedBefore = 0

    # Fill background
    window.fill(BACKGROUND)

    # Draw the lines on screen
    xLineAmount = int(window_width * pow(10, zoom) / gridLength)  + (window_width % gridLength > 0)
    for i in range(xLineAmount):
        pygame.draw.line(window, LINECOLOUR, (gridToScreenX(0) % (gridLength * pow(0.1, zoom)) + i * gridLength * pow(0.1, zoom), 0), (gridToScreenX(0) % (gridLength * pow(0.1, zoom)) + i * gridLength * pow(0.1, zoom), window_height))

    yLineAmount = int(window_height * pow(10, zoom) / gridLength)  + (window_height % gridLength > 0)
    for i in range(yLineAmount):
        pygame.draw.line(window, LINECOLOUR, (0, gridToScreenY(0) % (gridLength * pow(0.1, zoom)) + i * gridLength * pow(0.1, zoom)), (window_width, gridToScreenY(0) % (gridLength * pow(0.1, zoom)) + i * gridLength * pow(0.1, zoom)))

    # Draw Circle at Center
    pygame.draw.circle(window, BLACK, (gridToScreenX(0), gridToScreenY(0)), circleSize, 0)
    
    # Draw the components
    PlaceComponent.display_components(window, window_width, window_height, gridToScreenX, gridToScreenY)



    UI.ShowToolBar(window, window_width, window_height, globalState.component)
    
    # Update the display
    pygame.display.flip()

# Quit Pygame

pygame.quit()
sys.exit()
