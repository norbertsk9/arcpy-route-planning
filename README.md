# ArcMap Route Optimization Toolbox

## Project Description

During my university studies, I developed a toolbox for ArcMap. This toolbox allows users to input a shapefile containing road data, including one-way streets and road closures. It provides two main functionalities:

1. **Fastest Route Calculation**: Users can find the fastest route based on the road class (e.g., highway, expressway, or rural road).
2. **Shortest Route Calculation**: Users can find the shortest route between two points.

This toolbox simplifies route optimization and makes it accessible to ArcMap users, enabling them to analyze and plan routes efficiently.

## Features

- **Fastest Route Calculation**: Determine the fastest route based on road class.
- **Shortest Route Calculation**: Find the shortest route between two points.
- **One-Way Streets**: Handle one-way streets in route calculations.
- **Road Closures**: Account for road closures in route calculations.
- **Custom Output**: Choose an output path and name for the route layer.
- **Traffic Jam Simulation (Optional)**: Simulate traffic jams on routes.

[Toolbox Screenshot](img/toolbox_img.jpg)

[Result of toolbox Screenshot](img/plan_route.jpg)
*The green line represents the fastest route. The blue-colored roads are congested, and the red path is the fastest route, bypassing the congested roads marked in blue along the fastest route, so it had to detour those streets.*

## Getting Started

### Prerequisites

- ArcMap installed on your system.

### Installation

1. Download the toolbox file.
2. Open ArcMap.
3. In the ArcMap interface, open the "Geoprocessing" menu and select "ArcToolbox."
4. Right-click on "ArcToolbox" and choose "Add Toolbox."
5. Browse to the downloaded toolbox file and select it.
6. The toolbox should now be available in ArcMap under "Custom Toolbox."

## Usage

1. Load your road data as a shapefile into ArcMap.
2. Open the "ArcMap Route Optimization Toolbox" from the "Custom Toolbox" in ArcMap.
3. Select the road layer, starting and ending points, and the route type (fastest or shortest).
4. Define the output path and name for the route layer.
5. Optionally, specify the presence of a traffic jam on the route.
6. Run the toolbox to calculate and visualize the optimized route.

## Contributing

If you'd like to contribute to this project, please follow our [contribution guidelines](CONTRIBUTING.md).