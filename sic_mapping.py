
# https://en.wikipedia.org/wiki/Standard_Industrial_Classification
wiki_table = """
    <tr>
    <td>0100
    </td>
    <td>Agricultural Production-Crops
    </td></tr>
    <tr>
    <td>0200
    </td>
    <td>Agricultural Prod-Livestock & Animal Specialties
    </td></tr>
    <tr>
    <td>0700
    </td>
    <td>Agricultural Services
    </td></tr>
    <tr>
    <td>0800
    </td>
    <td>Forestry
    </td></tr>
    <tr>
    <td>0900
    </td>
    <td>Fishing, Hunting and Trapping
    </td></tr>
    <tr>
    <td>1000
    </td>
    <td>Metal Mining
    </td></tr>
    <tr>
    <td>1040
    </td>
    <td>Gold and Silver Ores
    </td></tr>
    <tr>
    <td>1090
    </td>
    <td>Miscellaneous Metal Ores
    </td></tr>
    <tr>
    <td>1220
    </td>
    <td>Bituminous Coal & Lignite Mining
    </td></tr>
    <tr>
    <td>1221
    </td>
    <td>Bituminous Coal & Lignite Surface Mining
    </td></tr>
    <tr>
    <td>1311
    </td>
    <td>Crude Petroleum & Natural Gas
    </td></tr>
    <tr>
    <td>1381
    </td>
    <td>Drilling Oil & Gas Wells
    </td></tr>
    <tr>
    <td>1382
    </td>
    <td>Oil & Gas Field Exploration Services
    </td></tr>
    <tr>
    <td>1389
    </td>
    <td>Oil & Gas Field Services, NEC
    </td></tr>
    <tr>
    <td>1400
    </td>
    <td>Mining & Quarrying of Nonmetallic Minerals (No Fuels)
    </td></tr>
    <tr>
    <td>1520
    </td>
    <td>General Bldg Contractors - Residential Bldgs
    </td></tr>
    <tr>
    <td>1531
    </td>
    <td>Operative Builders
    </td></tr>
    <tr>
    <td>1540
    </td>
    <td>General Bldg Contractors - Nonresidential Bldgs
    </td></tr>
    <tr>
    <td>1600
    </td>
    <td>Heavy Construction Other Than Bldg Const - Contractors
    </td></tr>
    <tr>
    <td>1623
    </td>
    <td>Water, Sewer, Pipeline, Comm & Power Line Construction
    </td></tr>
    <tr>
    <td>1629
    </td>
    <td>Heavy Construction, Not Elsewhere Classified
    </td></tr>
    <tr>
    <td>1700
    </td>
    <td>Construction - Special Trade Contractors
    </td></tr>
    <tr>
    <td>1731
    </td>
    <td>Electrical Work
    </td></tr>
    <tr>
    <td>2000
    </td>
    <td>Food and Kindred Products
    </td></tr>
    <tr>
    <td>2011
    </td>
    <td>Meat Packing Plants
    </td></tr>
    <tr>
    <td>2013
    </td>
    <td>Sausages & Other Prepared Meat Products
    </td></tr>
    <tr>
    <td>2015
    </td>
    <td>Poultry Slaughtering and Processing
    </td></tr>
    <tr>
    <td>2020
    </td>
    <td>Dairy Products
    </td></tr>
    <tr>
    <td>2024
    </td>
    <td>Ice Cream & Frozen Desserts
    </td></tr>
    <tr>
    <td>2030
    </td>
    <td>Canned, Frozen & Preserved Fruit, Veg & Food Specialties
    </td></tr>
    <tr>
    <td>2033
    </td>
    <td>Canned, Fruits, Veg, Preserves, Jams & Jellies
    </td></tr>
    <tr>
    <td>2040
    </td>
    <td>Grain Mill Products
    </td></tr>
    <tr>
    <td>2050
    </td>
    <td>Bakery Products
    </td></tr>
    <tr>
    <td>2052
    </td>
    <td>Cookies & Crackers
    </td></tr>
    <tr>
    <td>2060
    </td>
    <td>Sugar & Confectionery Products
    </td></tr>
    <tr>
    <td>2070
    </td>
    <td>Fats & Oils
    </td></tr>
    <tr>
    <td>2080
    </td>
    <td>Beverages
    </td></tr>
    <tr>
    <td>2082
    </td>
    <td>Malt Beverages
    </td></tr>
    <tr>
    <td>2086
    </td>
    <td>Bottled & Canned Soft Drinks & Carbonated Waters
    </td></tr>
    <tr>
    <td>2090
    </td>
    <td>Miscellaneous Food Preparations & Kindred Products
    </td></tr>
    <tr>
    <td>2092
    </td>
    <td>Prepared Fresh or Frozen Fish & Seafood
    </td></tr>
    <tr>
    <td>2100
    </td>
    <td>Tobacco Products
    </td></tr>
    <tr>
    <td>2111
    </td>
    <td>Cigarettes
    </td></tr>
    <tr>
    <td>2200
    </td>
    <td>Textile Mill Products
    </td></tr>
    <tr>
    <td>2211
    </td>
    <td>Broadwoven Fabric Mills, Cotton
    </td></tr>
    <tr>
    <td>2221
    </td>
    <td>Broadwoven Fabric Mills, Man Made Fiber & Silk
    </td></tr>
    <tr>
    <td>2250
    </td>
    <td>Knitting Mills
    </td></tr>
    <tr>
    <td>2253
    </td>
    <td>Knit Outerwear Mills
    </td></tr>
    <tr>
    <td>2273
    </td>
    <td>Carpets & Rugs
    </td></tr>
    <tr>
    <td>2300
    </td>
    <td>Apparel & Other Finished Prods of Fabrics & Similar Matl
    </td></tr>
    <tr>
    <td>2320
    </td>
    <td>Men's & Boys' Furnishings, Work Clothing, & Allied Garments
    </td></tr>
    <tr>
    <td>2330
    </td>
    <td>Women's, Misses', and Juniors Outerwear
    </td></tr>
    <tr>
    <td>2340
    </td>
    <td>Women's, Misses', Children's & Infant's Undergarments
    </td></tr>
    <tr>
    <td>2390
    </td>
    <td>Miscellaneous Fabricated Textile Products
    </td></tr>
    <tr>
    <td>2400
    </td>
    <td>Lumber & Wood Products (No Furniture)
    </td></tr>
    <tr>
    <td>2421
    </td>
    <td>Sawmills & Planing Mills, General
    </td></tr>
    <tr>
    <td>2430
    </td>
    <td>Millwood, Veneer, Plywood, & Structural Wood Members
    </td></tr>
    <tr>
    <td>2451
    </td>
    <td>Mobile Homes
    </td></tr>
    <tr>
    <td>2452
    </td>
    <td>Prefabricated Wood Bldgs & Components
    </td></tr>
    <tr>
    <td>2510
    </td>
    <td>Household Furniture
    </td></tr>
    <tr>
    <td>2511
    </td>
    <td>Wood Household Furniture, (No Upholstered)
    </td></tr>
    <tr>
    <td>2520
    </td>
    <td>Office Furniture
    </td></tr>
    <tr>
    <td>2522
    </td>
    <td>Office Furniture (No Wood)
    </td></tr>
    <tr>
    <td>2531
    </td>
    <td>Public Bldg & Related Furniture
    </td></tr>
    <tr>
    <td>2540
    </td>
    <td>Partitions, Shelvg, Lockers, & office & Store Fixtures
    </td></tr>
    <tr>
    <td>2590
    </td>
    <td>Miscellaneous Furniture & Fixtures
    </td></tr>
    <tr>
    <td>2600
    </td>
    <td>Papers & Allied Products
    </td></tr>
    <tr>
    <td>2611
    </td>
    <td>Pulp Mills
    </td></tr>
    <tr>
    <td>2621
    </td>
    <td>Paper Mills
    </td></tr>
    <tr>
    <td>2631
    </td>
    <td>Paperboard Mills
    </td></tr>
    <tr>
    <td>2650
    </td>
    <td>Paperboard Containers & Boxes
    </td></tr>
    <tr>
    <td>2670
    </td>
    <td>Converted Paper & Paperboard Prods (No Containers/Boxes)
    </td></tr>
    <tr>
    <td>2673
    </td>
    <td>Plastics, Foil & Coated Paper Bags
    </td></tr>
    <tr>
    <td>2711
    </td>
    <td>Newspapers: Publishing or Publishing & Printing
    </td></tr>
    <tr>
    <td>2721
    </td>
    <td>Periodicals: Publishing or Publishing & Printing
    </td></tr>
    <tr>
    <td>2731
    </td>
    <td>Books: Publishing or Publishing & Printing
    </td></tr>
    <tr>
    <td>2732
    </td>
    <td>Book Printing
    </td></tr>
    <tr>
    <td>2741
    </td>
    <td>Miscellaneous Publishing
    </td></tr>
    <tr>
    <td>2750
    </td>
    <td>Commercial Printing
    </td></tr>
    <tr>
    <td>2761
    </td>
    <td>Manifold Business Forms
    </td></tr>
    <tr>
    <td>2771
    </td>
    <td>Greeting Cards
    </td></tr>
    <tr>
    <td>2780
    </td>
    <td>Blankbooks, Looseleaf Binders & Bookbinding & Related Work
    </td></tr>
    <tr>
    <td>2790
    </td>
    <td>Service Industries For The Printing Trade
    </td></tr>
    <tr>
    <td>2800
    </td>
    <td>Chemicals & Allied Products
    </td></tr>
    <tr>
    <td>2810
    </td>
    <td>Industrial Inorganic Chemicals
    </td></tr>
    <tr>
    <td>2820
    </td>
    <td>Plastic Material, Synth Resin/Rubber, Cellulos (No Glass)
    </td></tr>
    <tr>
    <td>2821
    </td>
    <td>Plastic Materials, Synth Resins & Nonvulcan Elastomers
    </td></tr>
    <tr>
    <td>2833
    </td>
    <td>Medicinal Chemicals & Botanical Products
    </td></tr>
    <tr>
    <td>2834
    </td>
    <td>Pharmaceutical Preparations
    </td></tr>
    <tr>
    <td>2835
    </td>
    <td>In Vitro & In Vivo Diagnostic Substances
    </td></tr>
    <tr>
    <td>2836
    </td>
    <td>Biological Products, (No Diagnostic Substances)
    </td></tr>
    <tr>
    <td>2840
    </td>
    <td>Soap, Detergents, Cleaning Preparations, Perfumes, Cosmetics
    </td></tr>
    <tr>
    <td>2842
    </td>
    <td>Specialty Cleaning, Polishing and Sanitation Preparations
    </td></tr>
    <tr>
    <td>2844
    </td>
    <td>Perfumes, Cosmetics & Other Toilet Preparations
    </td></tr>
    <tr>
    <td>2851
    </td>
    <td>Paints, Varnishes, Lacquers, Enamels & Allied Prods
    </td></tr>
    <tr>
    <td>2860
    </td>
    <td>Industrial Organic Chemicals
    </td></tr>
    <tr>
    <td>2870
    </td>
    <td>Agricultural Chemicals
    </td></tr>
    <tr>
    <td>2890
    </td>
    <td>Miscellaneous Chemical Products
    </td></tr>
    <tr>
    <td>2891
    </td>
    <td>Adhesives & Sealants
    </td></tr>
    <tr>
    <td>2911
    </td>
    <td>Petroleum Refining
    </td></tr>
    <tr>
    <td>2950
    </td>
    <td>Asphalt Paving & Roofing Materials
    </td></tr>
    <tr>
    <td>2990
    </td>
    <td>Miscellaneous Products of Petroleum & Coal
    </td></tr>
    <tr>
    <td>3011
    </td>
    <td>Tires & Inner Tubes
    </td></tr>
    <tr>
    <td>3021
    </td>
    <td>Rubber & Plastics Footwear
    </td></tr>
    <tr>
    <td>3050
    </td>
    <td>Gaskets, Packg & Sealg Devices & Rubber & Plastics Hose
    </td></tr>
    <tr>
    <td>3060
    </td>
    <td>Fabricated Rubber Products, NEC
    </td></tr>
    <tr>
    <td>3080
    </td>
    <td>Miscellaneous Plastics Products
    </td></tr>
    <tr>
    <td>3081
    </td>
    <td>Unsupported Plastics Film & Sheet
    </td></tr>
    <tr>
    <td>3086
    </td>
    <td>Plastics Foam Products
    </td></tr>
    <tr>
    <td>3089
    </td>
    <td>Plastics Products, NEC
    </td></tr>
    <tr>
    <td>3100
    </td>
    <td>Leather & Leather Products
    </td></tr>
    <tr>
    <td>3140
    </td>
    <td>Footwear, (No Rubber)
    </td></tr>
    <tr>
    <td>3211
    </td>
    <td>Flat Glass
    </td></tr>
    <tr>
    <td>3220
    </td>
    <td>Glass & Glassware, Pressed or Blown
    </td></tr>
    <tr>
    <td>3221
    </td>
    <td>Glass Containers
    </td></tr>
    <tr>
    <td>3231
    </td>
    <td>Glass Products, Made of Purchased Glass
    </td></tr>
    <tr>
    <td>3241
    </td>
    <td>Cement, Hydraulic
    </td></tr>
    <tr>
    <td>3250
    </td>
    <td>Structural Clay Products
    </td></tr>
    <tr>
    <td>3260
    </td>
    <td>Pottery & Related Products
    </td></tr>
    <tr>
    <td>3270
    </td>
    <td>Concrete, Gypsum & Plaster Products
    </td></tr>
    <tr>
    <td>3272
    </td>
    <td>Concrete Products, Except Block & Brick
    </td></tr>
    <tr>
    <td>3281
    </td>
    <td>Cut Stone & Stone Products
    </td></tr>
    <tr>
    <td>3290
    </td>
    <td>Abrasive, Asbestos & Misc Nonmetallic Mineral Prods
    </td></tr>
    <tr>
    <td>3310
    </td>
    <td>Steel Works, Blast Furnaces & Rolling & Finishing Mills
    </td></tr>
    <tr>
    <td>3312
    </td>
    <td>Steel Works, Blast Furnaces & Rolling Mills (Coke Ovens)
    </td></tr>
    <tr>
    <td>3317
    </td>
    <td>Steel Pipe & Tubes
    </td></tr>
    <tr>
    <td>3320
    </td>
    <td>Iron & Steel Foundries
    </td></tr>
    <tr>
    <td>3330
    </td>
    <td>Primary Smelting & Refining of Nonferrous Metals
    </td></tr>
    <tr>
    <td>3334
    </td>
    <td>Primary Production of Aluminum
    </td></tr>
    <tr>
    <td>3341
    </td>
    <td>Secondary Smelting & Refining of Nonferrous Metals
    </td></tr>
    <tr>
    <td>3350
    </td>
    <td>Rolling Drawing & Extruding of Nonferrous Metals
    </td></tr>
    <tr>
    <td>3357
    </td>
    <td>Drawing & Insulating of Nonferrous Wire
    </td></tr>
    <tr>
    <td>3360
    </td>
    <td>Nonferrous Foundries (Castings)
    </td></tr>
    <tr>
    <td>3390
    </td>
    <td>Miscellaneous Primary Metal Products
    </td></tr>
    <tr>
    <td>3411
    </td>
    <td>Metal Cans
    </td></tr>
    <tr>
    <td>3412
    </td>
    <td>Metal Shipping Barrels, Drums, Kegs & Pails
    </td></tr>
    <tr>
    <td>3420
    </td>
    <td>Cutlery, Handtools & General Hardware
    </td></tr>
    <tr>
    <td>3430
    </td>
    <td>Heating Equip, Except Elec & Warm Air; & Plumbing Fixtures
    </td></tr>
    <tr>
    <td>3433
    </td>
    <td>Heating Equipment, Except Electric & Warm Air Furnaces
    </td></tr>
    <tr>
    <td>3440
    </td>
    <td>Fabricated Structural Metal Products
    </td></tr>
    <tr>
    <td>3442
    </td>
    <td>Metal Doors, Sash, Frames, Moldings & Trim
    </td></tr>
    <tr>
    <td>3443
    </td>
    <td>Fabricated Plate Work (Boiler Shops)
    </td></tr>
    <tr>
    <td>3444
    </td>
    <td>Sheet Metal Work
    </td></tr>
    <tr>
    <td>3448
    </td>
    <td>Prefabricated Metal Buildings & Components
    </td></tr>
    <tr>
    <td>3451
    </td>
    <td>Screw Machine Products
    </td></tr>
    <tr>
    <td>3452
    </td>
    <td>Bolts, Nuts, Screws, Rivets & Washers
    </td></tr>
    <tr>
    <td>3460
    </td>
    <td>Metal Forgings & Stampings
    </td></tr>
    <tr>
    <td>3470
    </td>
    <td>Coating, Engraving & Allied Services
    </td></tr>
    <tr>
    <td>3480
    </td>
    <td>Ordnance & Accessories, (No Vehicles/Guided Missiles)
    </td></tr>
    <tr>
    <td>3490
    </td>
    <td>Miscellaneous Fabricated Metal Products
    </td></tr>
    <tr>
    <td>3510
    </td>
    <td>Engines & Turbines
    </td></tr>
    <tr>
    <td>3523
    </td>
    <td>Farm Machinery & Equipment
    </td></tr>
    <tr>
    <td>3524
    </td>
    <td>Lawn & Garden Tractors & Home Lawn & Gardens Equip
    </td></tr>
    <tr>
    <td>3530
    </td>
    <td>Construction, Mining & Materials Handling Machinery & Equip
    </td></tr>
    <tr>
    <td>3531
    </td>
    <td>Construction Machinery & Equip
    </td></tr>
    <tr>
    <td>3532
    </td>
    <td>Mining Machinery & Equip (No Oil & Gas Field Mach & Equip)
    </td></tr>
    <tr>
    <td>3533
    </td>
    <td>Oil & Gas Field Machinery & Equipment
    </td></tr>
    <tr>
    <td>3537
    </td>
    <td>Industrial Trucks, Tractors, Trailers & Stackers
    </td></tr>
    <tr>
    <td>3540
    </td>
    <td>Metalworkg Machinery & Equipment
    </td></tr>
    <tr>
    <td>3541
    </td>
    <td>Machine Tools, Metal Cutting Types
    </td></tr>
    <tr>
    <td>3550
    </td>
    <td>Special Industry Machinery (No Metalworking Machinery)
    </td></tr>
    <tr>
    <td>3555
    </td>
    <td>Printing Trades Machinery & Equipment
    </td></tr>
    <tr>
    <td>3559
    </td>
    <td>Special Industry Machinery, NEC
    </td></tr>
    <tr>
    <td>3560
    </td>
    <td>General Industrial Machinery & Equipment
    </td></tr>
    <tr>
    <td>3561
    </td>
    <td>Pumps & Pumping Equipment
    </td></tr>
    <tr>
    <td>3562
    </td>
    <td>Ball & Roller Bearings
    </td></tr>
    <tr>
    <td>3564
    </td>
    <td>Industrial & Commercial Fans & Blowers & Air Purifying Equip
    </td></tr>
    <tr>
    <td>3567
    </td>
    <td>Industrial Process Furnaces & Ovens
    </td></tr>
    <tr>
    <td>3569
    </td>
    <td>General Industrial Machinery & Equipment, NEC
    </td></tr>
    <tr>
    <td>3570
    </td>
    <td>Computer & office Equipment
    </td></tr>
    <tr>
    <td>3571
    </td>
    <td>Electronic Computers
    </td></tr>
    <tr>
    <td>3572
    </td>
    <td>Computer Storage Devices
    </td></tr>
    <tr>
    <td>3575
    </td>
    <td>Computer Terminals
    </td></tr>
    <tr>
    <td>3576
    </td>
    <td>Computer Communications Equipment
    </td></tr>
    <tr>
    <td>3577
    </td>
    <td>Computer Peripheral Equipment, NEC
    </td></tr>
    <tr>
    <td>3578
    </td>
    <td>Calculating & Accounting Machines (No Electronic Computers)
    </td></tr>
    <tr>
    <td>3579
    </td>
    <td>Office Machines, NEC
    </td></tr>
    <tr>
    <td>3580
    </td>
    <td>Refrigeration & Service Industry Machinery
    </td></tr>
    <tr>
    <td>3585
    </td>
    <td>Air-Cond & Warm Air Heatg Equip & Comm & Indl Refrig Equip
    </td></tr>
    <tr>
    <td>3590
    </td>
    <td>Misc Industrial & Commercial Machinery & Equipment
    </td></tr>
    <tr>
    <td>3600
    </td>
    <td>Electronic & Other Electrical Equipment (No Computer Equip)
    </td></tr>
    <tr>
    <td>3612
    </td>
    <td>Power, Distribution & Specialty Transformers
    </td></tr>
    <tr>
    <td>3613
    </td>
    <td>Switchgear & Switchboard Apparatus
    </td></tr>
    <tr>
    <td>3620
    </td>
    <td>Electrical Industrial Apparatus
    </td></tr>
    <tr>
    <td>3621
    </td>
    <td>Motors & Generators
    </td></tr>
    <tr>
    <td>3630
    </td>
    <td>Household Appliances
    </td></tr>
    <tr>
    <td>3634
    </td>
    <td>Electric Housewares & Fans
    </td></tr>
    <tr>
    <td>3640
    </td>
    <td>Electric Lighting & Wiring Equipment
    </td></tr>
    <tr>
    <td>3651
    </td>
    <td>Household Audio & Video Equipment
    </td></tr>
    <tr>
    <td>3652
    </td>
    <td>Phonograph Records & Prerecorded Audio Tapes & Disks
    </td></tr>
    <tr>
    <td>3661
    </td>
    <td>Telephone & Telegraph Apparatus
    </td></tr>
    <tr>
    <td>3663
    </td>
    <td>Radio & TV Broadcasting & Communications Equipment
    </td></tr>
    <tr>
    <td>3669
    </td>
    <td>Communications Equipment, NEC
    </td></tr>
    <tr>
    <td>3670
    </td>
    <td>Electronic Components & Accessories
    </td></tr>
    <tr>
    <td>3672
    </td>
    <td>Printed Circuit Boards
    </td></tr>
    <tr>
    <td>3674
    </td>
    <td>Semiconductors & Related Devices
    </td></tr>
    <tr>
    <td>3677
    </td>
    <td>Electronic Coils, Transformers & Other Inductors
    </td></tr>
    <tr>
    <td>3678
    </td>
    <td>Electronic Connectors
    </td></tr>
    <tr>
    <td>3679
    </td>
    <td>Electronic Components, NEC
    </td></tr>
    <tr>
    <td>3690
    </td>
    <td>Miscellaneous Electrical Machinery, Equipment & Supplies
    </td></tr>
    <tr>
    <td>3695
    </td>
    <td>Magnetic & Optical Recording Media
    </td></tr>
    <tr>
    <td>3711
    </td>
    <td>Motor Vehicles & Passenger Car Bodies
    </td></tr>
    <tr>
    <td>3713
    </td>
    <td>Truck & Bus Bodies
    </td></tr>
    <tr>
    <td>3714
    </td>
    <td>Motor Vehicle Parts & Accessories
    </td></tr>
    <tr>
    <td>3715
    </td>
    <td>Truck Trailers
    </td></tr>
    <tr>
    <td>3716
    </td>
    <td>Motor Homes
    </td></tr>
    <tr>
    <td>3720
    </td>
    <td>Aircraft & Parts
    </td></tr>
    <tr>
    <td>3721
    </td>
    <td>Aircraft
    </td></tr>
    <tr>
    <td>3724
    </td>
    <td>Aircraft Engines & Engine Parts
    </td></tr>
    <tr>
    <td>3728
    </td>
    <td>Aircraft Parts & Auxiliary Equipment, NEC
    </td></tr>
    <tr>
    <td>3730
    </td>
    <td>Ship & Boat Building & Repairing
    </td></tr>
    <tr>
    <td>3743
    </td>
    <td>Railroad Equipment
    </td></tr>
    <tr>
    <td>3751
    </td>
    <td>Motorcycles, Bicycles & Parts
    </td></tr>
    <tr>
    <td>3760
    </td>
    <td>Guided Missiles & Space Vehicles & Parts
    </td></tr>
    <tr>
    <td>3790
    </td>
    <td>Miscellaneous Transportation Equipment
    </td></tr>
    <tr>
    <td>3812
    </td>
    <td>Search, Detection, Navigation, Guidance, Aeronautical Sys
    </td></tr>
    <tr>
    <td>3821
    </td>
    <td>Laboratory Apparatus & Furniture
    </td></tr>
    <tr>
    <td>3822
    </td>
    <td>Auto Controls For Regulating Residential & Comml Environments
    </td></tr>
    <tr>
    <td>3823
    </td>
    <td>Industrial Instruments For Measurement, Display, and Control
    </td></tr>
    <tr>
    <td>3824
    </td>
    <td>Totalizing Fluid Meters & Counting Devices
    </td></tr>
    <tr>
    <td>3825
    </td>
    <td>Instruments For Meas & Testing of Electricity & Elec Signals
    </td></tr>
    <tr>
    <td>3826
    </td>
    <td>Laboratory Analytical Instruments
    </td></tr>
    <tr>
    <td>3827
    </td>
    <td>Optical Instruments & Lenses
    </td></tr>
    <tr>
    <td>3829
    </td>
    <td>Measuring & Controlling Devices, NEC
    </td></tr>
    <tr>
    <td>3841
    </td>
    <td>Surgical & Medical Instruments & Apparatus
    </td></tr>
    <tr>
    <td>3842
    </td>
    <td>Orthopedic, Prosthetic & Surgical Appliances & Supplies
    </td></tr>
    <tr>
    <td>3843
    </td>
    <td>Dental Equipment & Supplies
    </td></tr>
    <tr>
    <td>3844
    </td>
    <td>X-Ray Apparatus & Tubes & Related Irradiation Apparatus
    </td></tr>
    <tr>
    <td>3845
    </td>
    <td>Electromedical & Electrotherapeutic Apparatus
    </td></tr>
    <tr>
    <td>3851
    </td>
    <td>Ophthalmic Goods
    </td></tr>
    <tr>
    <td>3861
    </td>
    <td>Photographic Equipment & Supplies
    </td></tr>
    <tr>
    <td>3873
    </td>
    <td>Watches, Clocks, Clockwork Operated Devices/Parts
    </td></tr>
    <tr>
    <td>3910
    </td>
    <td>Jewelry, Silverware & Plated Ware
    </td></tr>
    <tr>
    <td>3911
    </td>
    <td>Jewelry, Precious Metal
    </td></tr>
    <tr>
    <td>3931
    </td>
    <td>Musical Instruments
    </td></tr>
    <tr>
    <td>3942
    </td>
    <td>Dolls & Stuffed Toys
    </td></tr>
    <tr>
    <td>3944
    </td>
    <td>Games, Toys & Children's Vehicles (No Dolls & Bicycles)
    </td></tr>
    <tr>
    <td>3949
    </td>
    <td>Sporting & Athletic Goods, NEC
    </td></tr>
    <tr>
    <td>3950
    </td>
    <td>Pens, Pencils & Other Artists' Materials
    </td></tr>
    <tr>
    <td>3960
    </td>
    <td>Costume Jewelry & Novelties
    </td></tr>
    <tr>
    <td>3990
    </td>
    <td>Miscellaneous Manufacturing Industries
    </td></tr>
    <tr>
    <td>4011
    </td>
    <td>Railroads, Line-Haul Operating
    </td></tr>
    <tr>
    <td>4013
    </td>
    <td>Railroad Switching & Terminal Establishments
    </td></tr>
    <tr>
    <td>4100
    </td>
    <td>Local & Suburban Transit & Interurban Hwy Passenger Trans
    </td></tr>
    <tr>
    <td>4210
    </td>
    <td>Trucking & Courier Services (No Air)
    </td></tr>
    <tr>
    <td>4213
    </td>
    <td>Trucking (No Local)
    </td></tr>
    <tr>
    <td>4220
    </td>
    <td>Public Warehousing & Storage
    </td></tr>
    <tr>
    <td>4231
    </td>
    <td>Terminal Maintenance Facilities For Motor Freight Transport
    </td></tr>
    <tr>
    <td>4400
    </td>
    <td>Water Transportation
    </td></tr>
    <tr>
    <td>4412
    </td>
    <td>Deep Sea Foreign Transportation of Freight
    </td></tr>
    <tr>
    <td>4512
    </td>
    <td>Air Transportation, Scheduled
    </td></tr>
    <tr>
    <td>4513
    </td>
    <td>Air Courier Services
    </td></tr>
    <tr>
    <td>4522
    </td>
    <td>Air Transportation, Nonscheduled
    </td></tr>
    <tr>
    <td>4581
    </td>
    <td>Airports, Flying Fields & Airport Terminal Services
    </td></tr>
    <tr>
    <td>4610
    </td>
    <td>Pipe Lines (No Natural Gas)
    </td></tr>
    <tr>
    <td>4700
    </td>
    <td>Transportation Services
    </td></tr>
    <tr>
    <td>4731
    </td>
    <td>Arrangement of Transportation of Freight & Cargo
    </td></tr>
    <tr>
    <td>4812
    </td>
    <td>Radiotelephone Communications
    </td></tr>
    <tr>
    <td>4813
    </td>
    <td>Telephone Communications (No Radiotelephone)
    </td></tr>
    <tr>
    <td>4822
    </td>
    <td>Telegraph & Other Message Communications
    </td></tr>
    <tr>
    <td>4832
    </td>
    <td>Radio Broadcasting Stations
    </td></tr>
    <tr>
    <td>4833
    </td>
    <td>Television Broadcasting Stations
    </td></tr>
    <tr>
    <td>4841
    </td>
    <td>Cable & Other Pay Television Services
    </td></tr>
    <tr>
    <td>4899
    </td>
    <td>Communications Services, NEC
    </td></tr>
    <tr>
    <td>4900
    </td>
    <td>Electric, Gas & Sanitary Services
    </td></tr>
    <tr>
    <td>4911
    </td>
    <td>Electric Services
    </td></tr>
    <tr>
    <td>4922
    </td>
    <td>Natural Gas Transmission
    </td></tr>
    <tr>
    <td>4923
    </td>
    <td>Natural Gas Transmission & Distribution
    </td></tr>
    <tr>
    <td>4924
    </td>
    <td>Natural Gas Distribution
    </td></tr>
    <tr>
    <td>4931
    </td>
    <td>Electric & Other Services Combined
    </td></tr>
    <tr>
    <td>4932
    </td>
    <td>Gas & Other Services Combined
    </td></tr>
    <tr>
    <td>4941
    </td>
    <td>Water Supply
    </td></tr>
    <tr>
    <td>4950
    </td>
    <td>Sanitary Services
    </td></tr>
    <tr>
    <td>4953
    </td>
    <td>Refuse Systems
    </td></tr>
    <tr>
    <td>4955
    </td>
    <td>Hazardous Waste Management
    </td></tr>
    <tr>
    <td>4961
    </td>
    <td>Steam & Air-Conditioning Supply
    </td></tr>
    <tr>
    <td>4991
    </td>
    <td>Co-generation Services & Small Power Producers
    </td></tr>
    <tr>
    <td>5000
    </td>
    <td>Wholesale-Durable Goods
    </td></tr>
    <tr>
    <td>5010
    </td>
    <td>Wholesale-Motor Vehicles & Motor Vehicle Parts & Supplies
    </td></tr>
    <tr>
    <td>5013
    </td>
    <td>Wholesale-Motor Vehicle Supplies & New Parts
    </td></tr>
    <tr>
    <td>5020
    </td>
    <td>Wholesale-Furniture & Home Furnishings
    </td></tr>
    <tr>
    <td>5030
    </td>
    <td>Wholesale-Lumber & Other Construction Materials
    </td></tr>
    <tr>
    <td>5031
    </td>
    <td>Wholesale-Lumber, Plywood, millwork & Wood Panels
    </td></tr>
    <tr>
    <td>5040
    </td>
    <td>Wholesale-Professional & Commercial Equipment & Supplies
    </td></tr>
    <tr>
    <td>5045
    </td>
    <td>Wholesale-Computers & Peripheral Equipment & Software
    </td></tr>
    <tr>
    <td>5047
    </td>
    <td>Wholesale-Medical, Dental & Hospital Equipment & Supplies
    </td></tr>
    <tr>
    <td>5050
    </td>
    <td>Wholesale-Metals & Minerals (No Petroleum)
    </td></tr>
    <tr>
    <td>5051
    </td>
    <td>Wholesale-Metals Service Centers & Offices
    </td></tr>
    <tr>
    <td>5063
    </td>
    <td>Wholesale-Electrical Apparatus & Equipment, Wiring Supplies
    </td></tr>
    <tr>
    <td>5064
    </td>
    <td>Wholesale-Electrical Appliances, TV & Radio Sets
    </td></tr>
    <tr>
    <td>5065
    </td>
    <td>Wholesale-Electronic Parts & Equipment, NEC
    </td></tr>
    <tr>
    <td>5070
    </td>
    <td>Wholesale-Hardware & Plumbing & Heating Equipment & Supplies
    </td></tr>
    <tr>
    <td>5072
    </td>
    <td>Wholesale-Hardware
    </td></tr>
    <tr>
    <td>5080
    </td>
    <td>Wholesale-Machinery, Equipment & Supplies
    </td></tr>
    <tr>
    <td>5082
    </td>
    <td>Wholesale-Construction & Mining (No Petro) Machinery & Equip
    </td></tr>
    <tr>
    <td>5084
    </td>
    <td>Wholesale-Industrial Machinery & Equipment
    </td></tr>
    <tr>
    <td>5090
    </td>
    <td>Wholesale-Misc Durable Goods
    </td></tr>
    <tr>
    <td>5094
    </td>
    <td>Wholesale-Jewelry, Watches, Precious Stones & Metals
    </td></tr>
    <tr>
    <td>5099
    </td>
    <td>Wholesale-Durable Goods, NEC
    </td></tr>
    <tr>
    <td>5110
    </td>
    <td>Wholesale-Paper & Paper Products
    </td></tr>
    <tr>
    <td>5122
    </td>
    <td>Wholesale-Drugs, Proprietaries & Druggists' Sundries
    </td></tr>
    <tr>
    <td>5130
    </td>
    <td>Wholesale-Apparel, Piece Goods & Notions
    </td></tr>
    <tr>
    <td>5140
    </td>
    <td>Wholesale-Groceries & Related Products
    </td></tr>
    <tr>
    <td>5141
    </td>
    <td>Wholesale-Groceries, General Line (merchandise)
    </td></tr>
    <tr>
    <td>5150
    </td>
    <td>Wholesale-Farm Product Raw Materials
    </td></tr>
    <tr>
    <td>5160
    </td>
    <td>Wholesale-Chemicals & Allied Products
    </td></tr>
    <tr>
    <td>5171
    </td>
    <td>Wholesale-Petroleum Bulk Stations & Terminals
    </td></tr>
    <tr>
    <td>5172
    </td>
    <td>Wholesale-Petroleum & Petroleum Products (No Bulk Stations)
    </td></tr>
    <tr>
    <td>5180
    </td>
    <td>Wholesale-Beer, Wine & Distilled Alcoholic Beverages
    </td></tr>
    <tr>
    <td>5190
    </td>
    <td>Wholesale-Miscellaneous Non-durable Goods
    </td></tr>
    <tr>
    <td>5200
    </td>
    <td>Retail-Building Materials, Hardware, Garden Supply
    </td></tr>
    <tr>
    <td>5211
    </td>
    <td>Retail-Lumber & Other Building Materials Dealers
    </td></tr>
    <tr>
    <td>5271
    </td>
    <td>Retail-Mobile Home Dealers
    </td></tr>
    <tr>
    <td>5311
    </td>
    <td>Retail-Department Stores
    </td></tr>
    <tr>
    <td>5331
    </td>
    <td>Retail-Variety Stores
    </td></tr>
    <tr>
    <td>5399
    </td>
    <td>Retail-Misc General Merchandise Stores
    </td></tr>
    <tr>
    <td>5400
    </td>
    <td>Retail-Food Stores
    </td></tr>
    <tr>
    <td>5411
    </td>
    <td>Retail-Grocery Stores
    </td></tr>
    <tr>
    <td>5412
    </td>
    <td>Retail-Convenience Stores
    </td></tr>
    <tr>
    <td>5500
    </td>
    <td>Retail-Auto Dealers & Gasoline Stations
    </td></tr>
    <tr>
    <td>5531
    </td>
    <td>Retail-Auto & Home Supply Stores
    </td></tr>
    <tr>
    <td>5551
    </td>
    <td>Boat Dealers
    </td></tr>
    <tr>
    <td>5600
    </td>
    <td>Retail-Apparel & Accessory Stores
    </td></tr>
    <tr>
    <td>5621
    </td>
    <td>Retail-Women's Clothing Stores
    </td></tr>
    <tr>
    <td>5651
    </td>
    <td>Retail-Family Clothing Stores
    </td></tr>
    <tr>
    <td>5661
    </td>
    <td>Retail-Shoe Stores
    </td></tr>
    <tr>
    <td>5700
    </td>
    <td>Retail-Home Furniture, Furnishings & Equipment Stores
    </td></tr>
    <tr>
    <td>5712
    </td>
    <td>Retail-Furniture Stores
    </td></tr>
    <tr>
    <td>5731
    </td>
    <td>Retail-Radio, TV & Consumer Electronics Stores
    </td></tr>
    <tr>
    <td>5734
    </td>
    <td>Retail-Computer & Computer Software Stores
    </td></tr>
    <tr>
    <td>5735
    </td>
    <td>Retail-Record & Prerecorded Tape Stores
    </td></tr>
    <tr>
    <td>5810
    </td>
    <td>Retail-Eating & Drinking Places
    </td></tr>
    <tr>
    <td>5812
    </td>
    <td>Retail-Eating Places
    </td></tr>
    <tr>
    <td>5900
    </td>
    <td>Retail-Miscellaneous Retail
    </td></tr>
    <tr>
    <td>5912
    </td>
    <td>Retail-Drug Stores and Proprietary Stores
    </td></tr>
    <tr>
    <td>5940
    </td>
    <td>Retail-Miscellaneous Shopping Goods Stores
    </td></tr>
    <tr>
    <td>5944
    </td>
    <td>Retail-Jewelry Stores
    </td></tr>
    <tr>
    <td>5945
    </td>
    <td>Retail-Hobby, Toy & Game Shops
    </td></tr>
    <tr>
    <td>5960
    </td>
    <td>Retail-Nonstore Retailers
    </td></tr>
    <tr>
    <td>5961
    </td>
    <td>Retail-Catalog & Mail-Order Houses
    </td></tr>
    <tr>
    <td>5990
    </td>
    <td>Retail-Retail Stores, NEC
    </td></tr>
    <tr>
    <td>6012
    </td>
    <td>Pay Day Lenders
    </td></tr>
    <tr>
    <td>6021
    </td>
    <td>National Commercial Banks
    </td></tr>
    <tr>
    <td>6022
    </td>
    <td>State Commercial Banks
    </td></tr>
    <tr>
    <td>6029
    </td>
    <td>Commercial Banks, NEC
    </td></tr>
    <tr>
    <td>6035
    </td>
    <td>Savings Institution, Federally Chartered
    </td></tr>
    <tr>
    <td>6036
    </td>
    <td>Savings Institutions, Not Federally Chartered
    </td></tr>
    <tr>
    <td>6099
    </td>
    <td>Functions Related To Depository Banking, NEC
    </td></tr>
    <tr>
    <td>6111
    </td>
    <td>Federal & Federally Sponsored Credit Agencies
    </td></tr>
    <tr>
    <td>6141
    </td>
    <td>Personal Credit Institutions
    </td></tr>
    <tr>
    <td>6153
    </td>
    <td>Short-Term Business Credit Institutions
    </td></tr>
    <tr>
    <td>6159
    </td>
    <td>Miscellaneous Business Credit Institution
    </td></tr>
    <tr>
    <td>6162
    </td>
    <td>Mortgage Bankers & Loan Correspondents
    </td></tr>
    <tr>
    <td>6163
    </td>
    <td>Loan Brokers
    </td></tr>
    <tr>
    <td>6172
    </td>
    <td>Finance Lessors
    </td></tr>
    <tr>
    <td>6189
    </td>
    <td>Asset-Backed Securities
    </td></tr>
    <tr>
    <td>6199
    </td>
    <td>Finance Services
    </td></tr>
    <tr>
    <td>6200
    </td>
    <td>Security & Commodity Brokers, Dealers, Exchanges & Services
    </td></tr>
    <tr>
    <td>6211
    </td>
    <td>Security Brokers, Dealers & Flotation Companies
    </td></tr>
    <tr>
    <td>6221
    </td>
    <td>Commodity Contracts Brokers & Dealers
    </td></tr>
    <tr>
    <td>6282
    </td>
    <td>Investment Advice
    </td></tr>
    <tr>
    <td>6311
    </td>
    <td>Life Insurance
    </td></tr>
    <tr>
    <td>6321
    </td>
    <td>Accident & Health Insurance
    </td></tr>
    <tr>
    <td>6324
    </td>
    <td>Hospital & Medical Service Plans
    </td></tr>
    <tr>
    <td>6331
    </td>
    <td>Fire, Marine & Casualty Insurance
    </td></tr>
    <tr>
    <td>6351
    </td>
    <td>Surety Insurance
    </td></tr>
    <tr>
    <td>6361
    </td>
    <td>Title Insurance
    </td></tr>
    <tr>
    <td>6399
    </td>
    <td>Insurance Carriers, NEC
    </td></tr>
    <tr>
    <td>6411
    </td>
    <td>Insurance Agents, Brokers & Service
    </td></tr>
    <tr>
    <td>6500
    </td>
    <td>Real Estate
    </td></tr>
    <tr>
    <td>6510
    </td>
    <td>Real Estate Operators (No Developers) & Lessors
    </td></tr>
    <tr>
    <td>6512
    </td>
    <td>Operators of Nonresidential Buildings
    </td></tr>
    <tr>
    <td>6513
    </td>
    <td>Operators of Apartment Buildings
    </td></tr>
    <tr>
    <td>6519
    </td>
    <td>Lessors of Real Property, NEC
    </td></tr>
    <tr>
    <td>6531
    </td>
    <td>Real Estate Agents & Managers (For Others)
    </td></tr>
    <tr>
    <td>6532
    </td>
    <td>Real Estate Dealers (For Their Own Account)
    </td></tr>
    <tr>
    <td>6552
    </td>
    <td>Land Subdividers & Developers (No Cemeteries)
    </td></tr>
    <tr>
    <td>6770
    </td>
    <td>Blank Checks
    </td></tr>
    <tr>
    <td>6792
    </td>
    <td>Oil Royalty Traders
    </td></tr>
    <tr>
    <td>6794
    </td>
    <td>Patent Owners & Lessors
    </td></tr>
    <tr>
    <td>6795
    </td>
    <td>Mineral Royalty Traders
    </td></tr>
    <tr>
    <td>6798
    </td>
    <td>Real Estate Investment Trusts
    </td></tr>
    <tr>
    <td>6799
    </td>
    <td>Investors, NEC
    </td></tr>
    <tr>
    <td>7000
    </td>
    <td>Hotels, Rooming Houses, Camps & Other Lodging Places
    </td></tr>
    <tr>
    <td>7011
    </td>
    <td>Hotels & Motels
    </td></tr>
    <tr>
    <td>7200
    </td>
    <td>Services-Personal Services
    </td></tr>
    <tr>
    <td>7310
    </td>
    <td>Services-Advertising
    </td></tr>
    <tr>
    <td>7311
    </td>
    <td>Services-Advertising Agencies
    </td></tr>
    <tr>
    <td>7320
    </td>
    <td>Services-Consumer Credit Reporting, Collection Agencies
    </td></tr>
    <tr>
    <td>7330
    </td>
    <td>Services-Mailing, Reproduction, Commercial Art & Photography
    </td></tr>
    <tr>
    <td>7331
    </td>
    <td>Services-Direct Mail Advertising Services
    </td></tr>
    <tr>
    <td>7334
    </td>
    <td>Services-Photocopying and Duplicating Services
    </td></tr>
    <tr>
    <td>7340
    </td>
    <td>Services-To Dwellings & Other Buildings
    </td></tr>
    <tr>
    <td>7350
    </td>
    <td>Services-Miscellaneous Equipment Rental & Leasing
    </td></tr>
    <tr>
    <td>7359
    </td>
    <td>Services-Equipment Rental & Leasing, NEC
    </td></tr>
    <tr>
    <td>7361
    </td>
    <td>Services-Employment Agencies
    </td></tr>
    <tr>
    <td>7363
    </td>
    <td>Services-Help Supply Services
    </td></tr>
    <tr>
    <td>7370
    </td>
    <td>Services-Computer Programming, Data Processing, Etc.
    </td></tr>
    <tr>
    <td>7371
    </td>
    <td>Services-Computer Programming Services
    </td></tr>
    <tr>
    <td>7372
    </td>
    <td>Services-Prepackaged Software
    </td></tr>
    <tr>
    <td>7373
    </td>
    <td>Services-Computer Integrated Systems Design
    </td></tr>
    <tr>
    <td>7374
    </td>
    <td>Services-Computer Processing & Data Preparation
    </td></tr>
    <tr>
    <td>7377
    </td>
    <td>Services-Computer Rental & Leasing
    </td></tr>
    <tr>
    <td>7380
    </td>
    <td>Services-Miscellaneous Business Services
    </td></tr>
    <tr>
    <td>7381
    </td>
    <td>Services-Detective, Guard & Armored Car Services
    </td></tr>
    <tr>
    <td>7384
    </td>
    <td>Services-Photofinishing Laboratories
    </td></tr>
    <tr>
    <td>7385
    </td>
    <td>Services-Telephone Interconnect Systems
    </td></tr>
    <tr>
    <td>7389
    </td>
    <td>Services-Business Services, NEC
    </td></tr>
    <tr>
    <td>7500
    </td>
    <td>Services-Automotive Repair, Services & Parking
    </td></tr>
    <tr>
    <td>7510
    </td>
    <td>Services-Auto Rental & Leasing (No Drivers)
    </td></tr>
    <tr>
    <td>7600
    </td>
    <td>Services-Miscellaneous Repair Services
    </td></tr>
    <tr>
    <td>7812
    </td>
    <td>Services-Motion Picture & Video Tape Production
    </td></tr>
    <tr>
    <td>7819
    </td>
    <td>Services-Allied To Motion Picture Production
    </td></tr>
    <tr>
    <td>7822
    </td>
    <td>Services-Motion Picture & Video Tape Distribution
    </td></tr>
    <tr>
    <td>7829
    </td>
    <td>Services-Allied To Motion Picture Distribution
    </td></tr>
    <tr>
    <td>7830
    </td>
    <td>Services-Motion Picture Theaters
    </td></tr>
    <tr>
    <td>7841
    </td>
    <td>Services-Video Tape Rental
    </td></tr>
    <tr>
    <td>7900
    </td>
    <td>Services-Amusement & Recreation Services
    </td></tr>
    <tr>
    <td>7948
    </td>
    <td>Services-Racing, Including Track Operation
    </td></tr>
    <tr>
    <td>7990
    </td>
    <td>Services-Miscellaneous Amusement & Recreation
    </td></tr>
    <tr>
    <td>7994
    </td>
    <td>Services-Video Game Arcades
    </td></tr>
    <tr>
    <td>7995
    </td>
    <td>Services-Gambling Transactions
    </td></tr>
    <tr>
    <td>7996
    </td>
    <td>Services-Amusement Parks
    </td></tr>
    <tr>
    <td>7997
    </td>
    <td>Services-Membership Sports & Recreation Clubs
    </td></tr>
    <tr>
    <td>8000
    </td>
    <td>Services-Health Services
    </td></tr>
    <tr>
    <td>8011
    </td>
    <td>Services-Offices & Clinics of Doctors of Medicine
    </td></tr>
    <tr>
    <td>8050
    </td>
    <td>Services-Nursing & Personal Care Facilities
    </td></tr>
    <tr>
    <td>8051
    </td>
    <td>Services-Skilled Nursing Care Facilities
    </td></tr>
    <tr>
    <td>8060
    </td>
    <td>Services-Hospitals
    </td></tr>
    <tr>
    <td>8062
    </td>
    <td>Services-General Medical & Surgical Hospitals, NEC
    </td></tr>
    <tr>
    <td>8071
    </td>
    <td>Services-Medical Laboratories
    </td></tr>
    <tr>
    <td>8082
    </td>
    <td>Services-Home Health Care Services
    </td></tr>
    <tr>
    <td>8090
    </td>
    <td>Services-Misc Health & Allied Services, NEC
    </td></tr>
    <tr>
    <td>8093
    </td>
    <td>Services-Specialty Outpatient Facilities, NEC
    </td></tr>
    <tr>
    <td>8111
    </td>
    <td>Services-Legal Services
    </td></tr>
    <tr>
    <td>8200
    </td>
    <td>Services-Educational Services
    </td></tr>
    <tr>
    <td>8300
    </td>
    <td>Services-Social Services
    </td></tr>
    <tr>
    <td>8351
    </td>
    <td>Services-Child Day Care Services
    </td></tr>
    <tr>
    <td>8600
    </td>
    <td>Services-Membership organizations
    </td></tr>
    <tr>
    <td>8700
    </td>
    <td>Services-Engineering, Accounting, Research, Management
    </td></tr>
    <tr>
    <td>8711
    </td>
    <td>Services-Engineering Services
    </td></tr>
    <tr>
    <td>8731
    </td>
    <td>Services-Commercial Physical & Biological Research
    </td></tr>
    <tr>
    <td>8734
    </td>
    <td>Services-Testing Laboratories
    </td></tr>
    <tr>
    <td>8741
    </td>
    <td>Services-Management Services
    </td></tr>
    <tr>
    <td>8742
    </td>
    <td>Services-Management Consulting Services
    </td></tr>
    <tr>
    <td>8744
    </td>
    <td>Services-Facilities Support Management Services
    </td></tr>
    <tr>
    <td>8748
    </td>
    <td>Business Consulting Services, Not Elsewhere Classified
    </td></tr>
    <tr>
    <td>8880
    </td>
    <td>American Depositary Receipts
    </td></tr>
    <tr>
    <td>8888
    </td>
    <td>Foreign Governments
    </td></tr>
    <tr>
    <td>8900
    </td>
    <td>Services-Services, NEC
    </td></tr>
    <tr>
    <td>9721
    </td>
    <td>International Affairs
    </td></tr>
    <tr>
    <td>9995
    </td>
    <td>Non-Operating Establishments
    </td></tr>
"""

# https://sites.google.com/site/judsoncaskey/data
mapping = {

    1 :set(range(100,199 + 1)) | set(range(200,299 + 1)) | set(range(700,799 + 1)) | set(range(910,919 + 1)) | set(range(2048,2048 + 1)),
    2 :set(range(2000,2009 + 1)) | set(range(2010,2019 + 1)) | set(range(2020,2029 + 1)) | set(range(2030,2039 + 1)) | set(range(2040,2046 + 1)) | set(range(2050,2059 + 1)) | set(range(2060,2063 + 1)) | set(range(2070,2079 + 1)) | set(range(2090,2092 + 1)) | set(range(2095,2095 + 1)) | set(range(2098,2099 + 1)),
    3 :set(range(2064,2068 + 1)) | set(range(2086,2086 + 1)) | set(range(2087,2087 + 1)) | set(range(2096,2096 + 1)) | set(range(2097,2097 + 1)),
    4 :set(range(2080,2080 + 1)) | set(range(2082,2082 + 1)) | set(range(2083,2083 + 1)) | set(range(2084,2084 + 1)) | set(range(2085,2085 + 1)),
    5 :set(range(2100,2199 + 1)),
    6 :set(range(920,999 + 1)) | set(range(3650,3651 + 1)) | set(range(3652,3652 + 1)) | set(range(3732,3732 + 1)) | set(range(3930,3931 + 1)) | set(range(3940,3949 + 1)),
    7 :set(range(7800,7829 + 1)) | set(range(7830,7833 + 1)) | set(range(7840,7841 + 1)) | set(range(7900,7900 + 1)) | set(range(7910,7911 + 1)) | set(range(7920,7929 + 1)) | set(range(7930,7933 + 1)) | set(range(7940,7949 + 1)) | set(range(7980,7980 + 1)) | set(range(7990,7999 + 1)),
    8 :set(range(2700,2709 + 1)) | set(range(2710,2719 + 1)) | set(range(2720,2729 + 1)) | set(range(2730,2739 + 1)) | set(range(2740,2749 + 1)) | set(range(2770,2771 + 1)) | set(range(2780,2789 + 1)) | set(range(2790,2799 + 1)),
    9 :set(range(2047,2047 + 1)) | set(range(2391,2392 + 1)) | set(range(2510,2519 + 1)) | set(range(2590,2599 + 1)) | set(range(2840,2843 + 1)) | set(range(2844,2844 + 1)) | set(range(3160,3161 + 1)) | set(range(3170,3171 + 1)) | set(range(3172,3172 + 1)) | set(range(3190,3199 + 1)) | set(range(3229,3229 + 1)) | set(range(3260,3260 + 1)) | set(range(3262,3263 + 1)) | set(range(3269,3269 + 1)) | set(range(3230,3231 + 1)) | set(range(3630,3639 + 1)) | set(range(3750,3751 + 1)) | set(range(3800,3800 + 1)) | set(range(3860,3861 + 1)) | set(range(3870,3873 + 1)) | set(range(3910,3911 + 1)) | set(range(3914,3914 + 1)) | set(range(3915,3915 + 1)) | set(range(3960,3962 + 1)) | set(range(3991,3991 + 1)) | set(range(3995,3995 + 1)),
    10 :set(range(2300,2390 + 1)) | set(range(3020,3021 + 1)) | set(range(3100,3111 + 1)) | set(range(3130,3131 + 1)) | set(range(3140,3149 + 1)) | set(range(3150,3151 + 1)) | set(range(3963,3965 + 1)),
    11 :set(range(8000,8099 + 1)),
    12 :set(range(3693,3693 + 1)) | set(range(3840,3849 + 1)) | set(range(3850,3851 + 1)),
    13 :set(range(2830,2830 + 1)) | set(range(2831,2831 + 1)) | set(range(2833,2833 + 1)) | set(range(2834,2834 + 1)) | set(range(2835,2835 + 1)) | set(range(2836,2836 + 1)),
    14 :set(range(2800,2809 + 1)) | set(range(2810,2819 + 1)) | set(range(2820,2829 + 1)) | set(range(2850,2859 + 1)) | set(range(2860,2869 + 1)) | set(range(2870,2879 + 1)) | set(range(2890,2899 + 1)),
    15 :set(range(3031,3031 + 1)) | set(range(3041,3041 + 1)) | set(range(3050,3053 + 1)) | set(range(3060,3069 + 1)) | set(range(3070,3079 + 1)) | set(range(3080,3089 + 1)) | set(range(3090,3099 + 1)),
    16 :set(range(2200,2269 + 1)) | set(range(2270,2279 + 1)) | set(range(2280,2284 + 1)) | set(range(2290,2295 + 1)) | set(range(2297,2297 + 1)) | set(range(2298,2298 + 1)) | set(range(2299,2299 + 1)) | set(range(2393,2395 + 1)) | set(range(2397,2399 + 1)),
    17 :set(range(800,899 + 1)) | set(range(2400,2439 + 1)) | set(range(2450,2459 + 1)) | set(range(2490,2499 + 1)) | set(range(2660,2661 + 1)) | set(range(2950,2952 + 1)) | set(range(3200,3200 + 1)) | set(range(3210,3211 + 1)) | set(range(3240,3241 + 1)) | set(range(3250,3259 + 1)) | set(range(3261,3261 + 1)) | set(range(3264,3264 + 1)) | set(range(3270,3275 + 1)) | set(range(3280,3281 + 1)) | set(range(3290,3293 + 1)) | set(range(3295,3299 + 1)) | set(range(3420,3429 + 1)) | set(range(3430,3433 + 1)) | set(range(3440,3441 + 1)) | set(range(3442,3442 + 1)) | set(range(3446,3446 + 1)) | set(range(3448,3448 + 1)) | set(range(3449,3449 + 1)) | set(range(3450,3451 + 1)) | set(range(3452,3452 + 1)) | set(range(3490,3499 + 1)) | set(range(3996,3996 + 1)),
    18 :set(range(1500,1511 + 1)) | set(range(1520,1529 + 1)) | set(range(1530,1539 + 1)) | set(range(1540,1549 + 1)) | set(range(1600,1699 + 1)) | set(range(1700,1799 + 1)),
    19 :set(range(3300,3300 + 1)) | set(range(3310,3317 + 1)) | set(range(3320,3325 + 1)) | set(range(3330,3339 + 1)) | set(range(3340,3341 + 1)) | set(range(3350,3357 + 1)) | set(range(3360,3369 + 1)) | set(range(3370,3379 + 1)) | set(range(3390,3399 + 1)),
    20 :set(range(3400,3400 + 1)) | set(range(3443,3443 + 1)) | set(range(3444,3444 + 1)) | set(range(3460,3469 + 1)) | set(range(3470,3479 + 1)),
    21 :set(range(3510,3519 + 1)) | set(range(3520,3529 + 1)) | set(range(3530,3530 + 1)) | set(range(3531,3531 + 1)) | set(range(3532,3532 + 1)) | set(range(3533,3533 + 1)) | set(range(3534,3534 + 1)) | set(range(3535,3535 + 1)) | set(range(3536,3536 + 1)) | set(range(3538,3538 + 1)) | set(range(3540,3549 + 1)) | set(range(3550,3559 + 1)) | set(range(3560,3569 + 1)) | set(range(3580,3580 + 1)) | set(range(3581,3581 + 1)) | set(range(3582,3582 + 1)) | set(range(3585,3585 + 1)) | set(range(3586,3586 + 1)) | set(range(3589,3589 + 1)) | set(range(3590,3599 + 1)),
    22 :set(range(3600,3600 + 1)) | set(range(3610,3613 + 1)) | set(range(3620,3621 + 1)) | set(range(3623,3629 + 1)) | set(range(3640,3644 + 1)) | set(range(3645,3645 + 1)) | set(range(3646,3646 + 1)) | set(range(3648,3649 + 1)) | set(range(3660,3660 + 1)) | set(range(3690,3690 + 1)) | set(range(3691,3692 + 1)) | set(range(3699,3699 + 1)),
    23 :set(range(2296,2296 + 1)) | set(range(2396,2396 + 1)) | set(range(3010,3011 + 1)) | set(range(3537,3537 + 1)) | set(range(3647,3647 + 1)) | set(range(3694,3694 + 1)) | set(range(3700,3700 + 1)) | set(range(3710,3710 + 1)) | set(range(3711,3711 + 1)) | set(range(3713,3713 + 1)) | set(range(3714,3714 + 1)) | set(range(3715,3715 + 1)) | set(range(3716,3716 + 1)) | set(range(3792,3792 + 1)) | set(range(3790,3791 + 1)) | set(range(3799,3799 + 1)),
    24 :set(range(3720,3720 + 1)) | set(range(3721,3721 + 1)) | set(range(3723,3724 + 1)) | set(range(3725,3725 + 1)) | set(range(3728,3729 + 1)),
    25 :set(range(3730,3731 + 1)) | set(range(3740,3743 + 1)),
    26 :set(range(3760,3769 + 1)) | set(range(3795,3795 + 1)) | set(range(3480,3489 + 1)),
    27 :set(range(1040,1049 + 1)),
    28 :set(range(1000,1009 + 1)) | set(range(1010,1019 + 1)) | set(range(1020,1029 + 1)) | set(range(1030,1039 + 1)) | set(range(1050,1059 + 1)) | set(range(1060,1069 + 1)) | set(range(1070,1079 + 1)) | set(range(1080,1089 + 1)) | set(range(1090,1099 + 1)) | set(range(1100,1119 + 1)) | set(range(1400,1499 + 1)),
    29 :set(range(1200,1299 + 1)),
    30 :set(range(1300,1300 + 1)) | set(range(1310,1319 + 1)) | set(range(1320,1329 + 1)) | set(range(1330,1339 + 1)) | set(range(1370,1379 + 1)) | set(range(1380,1380 + 1)) | set(range(1381,1381 + 1)) | set(range(1382,1382 + 1)) | set(range(1389,1389 + 1)) | set(range(2900,2912 + 1)) | set(range(2990,2999 + 1)),
    31 :set(range(4900,4900 + 1)) | set(range(4910,4911 + 1)) | set(range(4920,4922 + 1)) | set(range(4923,4923 + 1)) | set(range(4924,4925 + 1)) | set(range(4930,4931 + 1)) | set(range(4932,4932 + 1)) | set(range(4939,4939 + 1)) | set(range(4940,4942 + 1)),
    32 :set(range(4800,4800 + 1)) | set(range(4810,4813 + 1)) | set(range(4820,4822 + 1)) | set(range(4830,4839 + 1)) | set(range(4840,4841 + 1)) | set(range(4880,4889 + 1)) | set(range(4890,4890 + 1)) | set(range(4891,4891 + 1)) | set(range(4892,4892 + 1)) | set(range(4899,4899 + 1)),
    33 :set(range(7020,7021 + 1)) | set(range(7030,7033 + 1)) | set(range(7200,7200 + 1)) | set(range(7210,7212 + 1)) | set(range(7214,7214 + 1)) | set(range(7215,7216 + 1)) | set(range(7217,7217 + 1)) | set(range(7219,7219 + 1)) | set(range(7220,7221 + 1)) | set(range(7230,7231 + 1)) | set(range(7240,7241 + 1)) | set(range(7250,7251 + 1)) | set(range(7260,7269 + 1)) | set(range(7270,7290 + 1)) | set(range(7291,7291 + 1)) | set(range(7292,7299 + 1)) | set(range(7395,7395 + 1)) | set(range(7500,7500 + 1)) | set(range(7520,7529 + 1)) | set(range(7530,7539 + 1)) | set(range(7540,7549 + 1)) | set(range(7600,7600 + 1)) | set(range(7620,7620 + 1)) | set(range(7622,7622 + 1)) | set(range(7623,7623 + 1)) | set(range(7629,7629 + 1)) | set(range(7630,7631 + 1)) | set(range(7640,7641 + 1)) | set(range(7690,7699 + 1)) | set(range(8100,8199 + 1)) | set(range(8200,8299 + 1)) | set(range(8300,8399 + 1)) | set(range(8400,8499 + 1)) | set(range(8600,8699 + 1)) | set(range(8800,8899 + 1)) | set(range(7510,7515 + 1)),
    34 :set(range(2750,2759 + 1)) | set(range(3993,3993 + 1)) | set(range(7218,7218 + 1)) | set(range(7300,7300 + 1)) | set(range(7310,7319 + 1)) | set(range(7320,7329 + 1)) | set(range(7330,7339 + 1)) | set(range(7340,7342 + 1)) | set(range(7349,7349 + 1)) | set(range(7350,7351 + 1)) | set(range(7352,7352 + 1)) | set(range(7353,7353 + 1)) | set(range(7359,7359 + 1)) | set(range(7360,7369 + 1)) | set(range(7370,7372 + 1)) | set(range(7374,7374 + 1)) | set(range(7375,7375 + 1)) | set(range(7376,7376 + 1)) | set(range(7377,7377 + 1)) | set(range(7378,7378 + 1)) | set(range(7379,7379 + 1)) | set(range(7380,7380 + 1)) | set(range(7381,7382 + 1)) | set(range(7383,7383 + 1)) | set(range(7384,7384 + 1)) | set(range(7385,7385 + 1)) | set(range(7389,7390 + 1)) | set(range(7391,7391 + 1)) | set(range(7392,7392 + 1)) | set(range(7393,7393 + 1)) | set(range(7394,7394 + 1)) | set(range(7396,7396 + 1)) | set(range(7397,7397 + 1)) | set(range(7399,7399 + 1)) | set(range(7519,7519 + 1)) | set(range(8700,8700 + 1)) | set(range(8710,8713 + 1)) | set(range(8720,8721 + 1)) | set(range(8730,8734 + 1)) | set(range(8740,8748 + 1)) | set(range(8900,8910 + 1)) | set(range(8911,8911 + 1)) | set(range(8920,8999 + 1)) | set(range(4220,4229 + 1)),
    35 :set(range(3570,3579 + 1)) | set(range(3680,3680 + 1)) | set(range(3681,3681 + 1)) | set(range(3682,3682 + 1)) | set(range(3683,3683 + 1)) | set(range(3684,3684 + 1)) | set(range(3685,3685 + 1)) | set(range(3686,3686 + 1)) | set(range(3687,3687 + 1)) | set(range(3688,3688 + 1)) | set(range(3689,3689 + 1)) | set(range(3695,3695 + 1)) | set(range(7373,7373 + 1)),
    36 :set(range(3622,3622 + 1)) | set(range(3661,3661 + 1)) | set(range(3662,3662 + 1)) | set(range(3663,3663 + 1)) | set(range(3664,3664 + 1)) | set(range(3665,3665 + 1)) | set(range(3666,3666 + 1)) | set(range(3669,3669 + 1)) | set(range(3670,3679 + 1)) | set(range(3810,3810 + 1)) | set(range(3812,3812 + 1)),
    37 :set(range(3811,3811 + 1)) | set(range(3820,3820 + 1)) | set(range(3821,3821 + 1)) | set(range(3822,3822 + 1)) | set(range(3823,3823 + 1)) | set(range(3824,3824 + 1)) | set(range(3825,3825 + 1)) | set(range(3826,3826 + 1)) | set(range(3827,3827 + 1)) | set(range(3829,3829 + 1)) | set(range(3830,3839 + 1)),
    38 :set(range(2520,2549 + 1)) | set(range(2600,2639 + 1)) | set(range(2670,2699 + 1)) | set(range(2760,2761 + 1)) | set(range(3950,3955 + 1)),
    39 :set(range(2440,2449 + 1)) | set(range(2640,2659 + 1)) | set(range(3220,3221 + 1)) | set(range(3410,3412 + 1)),
    40 :set(range(4000,4013 + 1)) | set(range(4040,4049 + 1)) | set(range(4100,4100 + 1)) | set(range(4110,4119 + 1)) | set(range(4120,4121 + 1)) | set(range(4130,4131 + 1)) | set(range(4140,4142 + 1)) | set(range(4150,4151 + 1)) | set(range(4170,4173 + 1)) | set(range(4190,4199 + 1)) | set(range(4200,4200 + 1)) | set(range(4210,4219 + 1)) | set(range(4230,4231 + 1)) | set(range(4240,4249 + 1)) | set(range(4400,4499 + 1)) | set(range(4500,4599 + 1)) | set(range(4600,4699 + 1)) | set(range(4700,4700 + 1)) | set(range(4710,4712 + 1)) | set(range(4720,4729 + 1)) | set(range(4730,4739 + 1)) | set(range(4740,4749 + 1)) | set(range(4780,4780 + 1)) | set(range(4782,4782 + 1)) | set(range(4783,4783 + 1)) | set(range(4784,4784 + 1)) | set(range(4785,4785 + 1)) | set(range(4789,4789 + 1)),
    41 :set(range(5000,5000 + 1)) | set(range(5010,5015 + 1)) | set(range(5020,5023 + 1)) | set(range(5030,5039 + 1)) | set(range(5040,5042 + 1)) | set(range(5043,5043 + 1)) | set(range(5044,5044 + 1)) | set(range(5045,5045 + 1)) | set(range(5046,5046 + 1)) | set(range(5047,5047 + 1)) | set(range(5048,5048 + 1)) | set(range(5049,5049 + 1)) | set(range(5050,5059 + 1)) | set(range(5060,5060 + 1)) | set(range(5063,5063 + 1)) | set(range(5064,5064 + 1)) | set(range(5065,5065 + 1)) | set(range(5070,5078 + 1)) | set(range(5080,5080 + 1)) | set(range(5081,5081 + 1)) | set(range(5082,5082 + 1)) | set(range(5083,5083 + 1)) | set(range(5084,5084 + 1)) | set(range(5085,5085 + 1)) | set(range(5086,5087 + 1)) | set(range(5088,5088 + 1)) | set(range(5090,5090 + 1)) | set(range(5091,5092 + 1)) | set(range(5093,5093 + 1)) | set(range(5094,5094 + 1)) | set(range(5099,5099 + 1)) | set(range(5100,5100 + 1)) | set(range(5110,5113 + 1)) | set(range(5120,5122 + 1)) | set(range(5130,5139 + 1)) | set(range(5140,5149 + 1)) | set(range(5150,5159 + 1)) | set(range(5160,5169 + 1)) | set(range(5170,5172 + 1)) | set(range(5180,5182 + 1)) | set(range(5190,5199 + 1)),
    42 :set(range(5200,5200 + 1)) | set(range(5210,5219 + 1)) | set(range(5220,5229 + 1)) | set(range(5230,5231 + 1)) | set(range(5250,5251 + 1)) | set(range(5260,5261 + 1)) | set(range(5270,5271 + 1)) | set(range(5300,5300 + 1)) | set(range(5310,5311 + 1)) | set(range(5320,5320 + 1)) | set(range(5330,5331 + 1)) | set(range(5334,5334 + 1)) | set(range(5340,5349 + 1)) | set(range(5390,5399 + 1)) | set(range(5400,5400 + 1)) | set(range(5410,5411 + 1)) | set(range(5412,5412 + 1)) | set(range(5420,5429 + 1)) | set(range(5430,5439 + 1)) | set(range(5440,5449 + 1)) | set(range(5450,5459 + 1)) | set(range(5460,5469 + 1)) | set(range(5490,5499 + 1)) | set(range(5500,5500 + 1)) | set(range(5510,5529 + 1)) | set(range(5530,5539 + 1)) | set(range(5540,5549 + 1)) | set(range(5550,5559 + 1)) | set(range(5560,5569 + 1)) | set(range(5570,5579 + 1)) | set(range(5590,5599 + 1)) | set(range(5600,5699 + 1)) | set(range(5700,5700 + 1)) | set(range(5710,5719 + 1)) | set(range(5720,5722 + 1)) | set(range(5730,5733 + 1)) | set(range(5734,5734 + 1)) | set(range(5735,5735 + 1)) | set(range(5736,5736 + 1)) | set(range(5750,5799 + 1)) | set(range(5900,5900 + 1)) | set(range(5910,5912 + 1)) | set(range(5920,5929 + 1)) | set(range(5930,5932 + 1)) | set(range(5940,5940 + 1)) | set(range(5941,5941 + 1)) | set(range(5942,5942 + 1)) | set(range(5943,5943 + 1)) | set(range(5944,5944 + 1)) | set(range(5945,5945 + 1)) | set(range(5946,5946 + 1)) | set(range(5947,5947 + 1)) | set(range(5948,5948 + 1)) | set(range(5949,5949 + 1)) | set(range(5950,5959 + 1)) | set(range(5960,5969 + 1)) | set(range(5970,5979 + 1)) | set(range(5980,5989 + 1)) | set(range(5990,5990 + 1)) | set(range(5992,5992 + 1)) | set(range(5993,5993 + 1)) | set(range(5994,5994 + 1)) | set(range(5995,5995 + 1)) | set(range(5999,5999 + 1)),
    43 :set(range(5800,5819 + 1)) | set(range(5820,5829 + 1)) | set(range(5890,5899 + 1)) | set(range(7000,7000 + 1)) | set(range(7010,7019 + 1)) | set(range(7040,7049 + 1)) | set(range(7213,7213 + 1)),
    44 :set(range(6000,6000 + 1)) | set(range(6010,6019 + 1)) | set(range(6020,6020 + 1)) | set(range(6021,6021 + 1)) | set(range(6022,6022 + 1)) | set(range(6023,6024 + 1)) | set(range(6025,6025 + 1)) | set(range(6026,6026 + 1)) | set(range(6027,6027 + 1)) | set(range(6028,6029 + 1)) | set(range(6030,6036 + 1)) | set(range(6040,6059 + 1)) | set(range(6060,6062 + 1)) | set(range(6080,6082 + 1)) | set(range(6090,6099 + 1)) | set(range(6100,6100 + 1)) | set(range(6110,6111 + 1)) | set(range(6112,6113 + 1)) | set(range(6120,6129 + 1)) | set(range(6130,6139 + 1)) | set(range(6140,6149 + 1)) | set(range(6150,6159 + 1)) | set(range(6160,6169 + 1)) | set(range(6170,6179 + 1)) | set(range(6190,6199 + 1)),
    45 :set(range(6300,6300 + 1)) | set(range(6310,6319 + 1)) | set(range(6320,6329 + 1)) | set(range(6330,6331 + 1)) | set(range(6350,6351 + 1)) | set(range(6360,6361 + 1)) | set(range(6370,6379 + 1)) | set(range(6390,6399 + 1)) | set(range(6400,6411 + 1)),
    46 :set(range(6500,6500 + 1)) | set(range(6510,6510 + 1)) | set(range(6512,6512 + 1)) | set(range(6513,6513 + 1)) | set(range(6514,6514 + 1)) | set(range(6515,6515 + 1)) | set(range(6517,6519 + 1)) | set(range(6520,6529 + 1)) | set(range(6530,6531 + 1)) | set(range(6532,6532 + 1)) | set(range(6540,6541 + 1)) | set(range(6550,6553 + 1)) | set(range(6590,6599 + 1)) | set(range(6610,6611 + 1)),
    47 :set(range(6200,6299 + 1)) | set(range(6700,6700 + 1)) | set(range(6710,6719 + 1)) | set(range(6720,6722 + 1)) | set(range(6723,6723 + 1)) | set(range(6724,6724 + 1)) | set(range(6725,6725 + 1)) | set(range(6726,6726 + 1)) | set(range(6730,6733 + 1)) | set(range(6740,6779 + 1)) | set(range(6790,6791 + 1)) | set(range(6792,6792 + 1)) | set(range(6793,6793 + 1)) | set(range(6794,6794 + 1)) | set(range(6795,6795 + 1)) | set(range(6798,6798 + 1)) | set(range(6799,6799 + 1)),
    48 : set(),
}

# https://sites.google.com/site/judsoncaskey/data
desc_mapping = {
    1: "Agriculture",
    2: "Food Products",
    3: "Candy & Soda",
    4: "Beer & Liquor",
    5: "Tobacco Products",
    6: "Recreation",
    7: "Entertainment",
    8: "Printing and Publishing",
    9: "Consumer Goods",
    10: "Apparel",
    11: "Healthcare",
    12: "Medical Equipment",
    13: "Pharmaceutical Products",
    14: "Chemicals",
    15: "Rubber and Plastic Products",
    16: "Textiles",
    17: "Construction Materials",
    18: "Construction",
    19: "Steel Works Etc",
    20: "Fabricated Products",
    21: "Machinery",
    22: "Electrical Equipment",
    23: "Automobiles and Trucks",
    24: "Aircraft",
    25: "Shipbuilding, Railroad Equipment",
    26: "Defense",
    27: "Precious Metals",
    28: "Non-Metallic and Industrial Metal Mining",
    29: "Coal",
    30: "Petroleum and Natural Gas",
    31: "Utilities",
    32: "Communication",
    33: "Personal Services",
    34: "Business Services",
    35: "Computers",
    36: "Electronic Equipment",
    37: "Measuring and Control Equipment",
    38: "Business Supplies",
    39: "Shipping Containers",
    40: "Transportation",
    41: "Wholesale",
    42: "Retail",
    43: "Restaraunts, Hotels, Motels",
    44: "Banking",
    45: "Insurance",
    46: "Real Estate", 
    47: "Trading",
    48: "Almost Nothing",
}

def get_ff_number(sic_code):
    for ff, code_set in mapping.items():
        if sic_code in code_set:
            return ff
    return 48

def sic_category():
    from bs4 import BeautifulSoup
    import json
    tree = BeautifulSoup(wiki_table, 'lxml')
    sic_cat = {}
    for tr in tree.find_all('tr'):
        code, category_name = tr.find_all('td')
        sic_cat[int(code.text)] = category_name.text.strip().replace('\n', '')
    for sic_number in range(100, 10000):
        # Use divisions as default values
        if sic_number in sic_cat:
            continue
        if sic_number < 1000:
            sic_cat[sic_number] = 'Agriculture, Forestry and Fishing'
        elif sic_number < 1500:
            sic_cat[sic_number] = 'Mining'
        elif sic_number < 1800:
            sic_cat[sic_number] = 'Construction'
        elif sic_number < 2000:
            sic_cat[sic_number] = 'not used'
        elif sic_number < 4000:
            sic_cat[sic_number] = 'Manufacturing'
        elif sic_number < 5000:
            sic_cat[sic_number] = 'Wholesale Trade'
        elif sic_number < 5200:
            sic_cat[sic_number] = 'Retail Trade'
        elif sic_number < 6000:
            sic_cat[sic_number] = 'Finance, Insurance and Real Estate'
        elif sic_number < 7000:
            sic_cat[sic_number] = 'Services'
        elif sic_number < 9100:
            sic_cat[sic_number] = 'Public Administration'
        elif sic_number < 10000:
            sic_cat[sic_number] = 'Nonclassifiable'
            
    return sic_cat

def sic_mapping_to_csv():
    import csv
    COLUMNS = ['SIC', 'FF_NUMBER', 'SIC_CATEGORY', 'FF_CATEGORY']
    sic_dict = sic_category()

    with open('sic_mapping.csv', 'w') as f_out:
        wr = csv.writer(f_out, lineterminator='\n', delimiter=';')
        wr.writerow(COLUMNS)
        for sic_number in range(100, 10000):
            ff_number = get_ff_number(sic_number)
            wr.writerow([sic_number, ff_number, sic_dict.get(sic_number), desc_mapping.get(ff_number)])


if __name__ == "__main__":
    sic_mapping_to_csv()