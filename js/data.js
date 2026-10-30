/*
 * Material data for the explorer.
 *
 * Scores are ILLUSTRATIVE DEMO VALUES copied from the Figma design (0–100).
 *   carbon:        lower is better
 *   recyclability: higher is better
 *   energy:        lower is better
 *
 * TODO: replace with the 15 materials + scores from the team's Excel sheet.
 *
 * `group` drives the filter chips; `family` is the label shown in the table.
 * `texture` is a CSS background used for the swatch and hero until real photos exist.
 * To use a real photo instead, add `image: "assets/materials/wood.jpg"`.
 */
window.MATERIAL_GROUPS = [
  { id: "all", label: "All materials" },
  { id: "metals", label: "Metals" },
  { id: "minerals", label: "Minerals" },
  { id: "polymers", label: "Polymers" },
  { id: "fibres", label: "Fibres & textiles" },
  { id: "other", label: "Other" },
];

window.MATERIALS = [
  {
    id: "steel",
    name: "Steel",
    family: "Metal",
    group: "metals",
    scores: { carbon: 72, recyclability: 88, energy: 76 },
    texture:
      "repeating-linear-gradient(90deg, rgba(255,255,255,.06) 0 1px, transparent 1px 3px), linear-gradient(135deg, #5b5d5f, #3a3c3e 60%, #4b4d4f)",
    description:
      "A strong iron-based alloy used in buildings, vehicles, tools and packaging. Recycled content and the furnace route change its impact.",
    tradeoff:
      "In this demo, steel is energy- and carbon-intensive to make, but it can be recycled repeatedly without losing strength, which makes long service life and recovery especially valuable.",
    tips: [
      "Ask for recycled content and the production route used.",
      "Design parts to be separated from coatings and plastics.",
      "Size sections to avoid using more steel than needed.",
    ],
  },
  {
    id: "glass",
    name: "Glass",
    family: "Mineral",
    group: "minerals",
    scores: { carbon: 54, recyclability: 82, energy: 68 },
    texture:
      "radial-gradient(circle at 30% 28%, rgba(255,255,255,.38), transparent 40%), radial-gradient(circle at 72% 72%, rgba(255,255,255,.18), transparent 35%), linear-gradient(135deg, #3f9a7c, #1f6b55 55%, #2f8a6c)",
    description:
      "A transparent material made by melting sand, soda ash and limestone. Used for windows, bottles, jars and screens.",
    tradeoff:
      "In this demo, glass needs high melting temperatures, but container glass recycles well when it is collected by colour and kept free of contamination.",
    tips: [
      "Prefer reusable containers over single-use ones.",
      "Avoid mixing glass with ceramics or bonded films.",
      "Check that local collection accepts the glass type.",
    ],
  },
  {
    id: "aluminium",
    name: "Aluminium",
    family: "Metal",
    group: "metals",
    scores: { carbon: 89, recyclability: 92, energy: 94 },
    texture:
      "repeating-linear-gradient(90deg, rgba(255,255,255,.22) 0 1px, transparent 1px 3px), linear-gradient(135deg, #dcdee0, #b3b6b9 55%, #cfd1d3)",
    description:
      "A light, corrosion-resistant metal used in cans, window frames, vehicles and electronics. Primary production is very electricity-intensive.",
    tradeoff:
      "In this demo, primary aluminium scores poorly on carbon and energy, yet recycled aluminium needs only a fraction of that energy, so recycled content matters more than almost anything else.",
    tips: [
      "Specify a high share of recycled aluminium.",
      "Ask about the electricity source used for smelting.",
      "Keep alloys and coatings simple to ease recycling.",
    ],
  },
  {
    id: "concrete",
    name: "Concrete",
    family: "Mineral",
    group: "minerals",
    scores: { carbon: 78, recyclability: 42, energy: 59 },
    texture:
      "radial-gradient(rgba(80,70,60,.35) 1px, transparent 1.6px) 0 0 / 7px 7px, radial-gradient(rgba(255,255,255,.28) 1px, transparent 1.6px) 3px 4px / 9px 9px, linear-gradient(135deg, #b9ab99, #9f927e)",
    description:
      "A mix of cement, water, sand and aggregate used for foundations, floors and structures. Cement is the main source of its impact.",
    tradeoff:
      "In this demo, concrete is durable and locally made, but cement production releases a lot of carbon, and crushed concrete is usually downcycled rather than reused as concrete.",
    tips: [
      "Ask for mixes with lower cement content or cement replacements.",
      "Avoid over-specifying strength and thickness.",
      "Plan for reuse of elements, not just demolition.",
    ],
  },
  {
    id: "plastic",
    name: "Plastic",
    family: "Polymer",
    group: "polymers",
    scores: { carbon: 67, recyclability: 31, energy: 71 },
    texture:
      "radial-gradient(ellipse at 30% 20%, rgba(255,255,255,.95), transparent 55%), linear-gradient(140deg, #efece6, #d4cfc6 60%, #e7e3dc)",
    description:
      "A broad family of fossil-based polymers moulded into packaging, housings and everyday products. Light, cheap and versatile.",
    tradeoff:
      "In this demo, plastic is light to transport, but most items are hard to recycle in practice because of mixed types, additives and food contamination.",
    tips: [
      "Use a single, clearly labelled polymer type.",
      "Avoid dark pigments and multi-layer laminates.",
      "Prefer durable, reusable items over disposable ones.",
    ],
  },
  {
    id: "paper",
    name: "Paper",
    family: "Fibre",
    group: "fibres",
    scores: { carbon: 36, recyclability: 78, energy: 43 },
    texture:
      "repeating-linear-gradient(35deg, rgba(160,140,110,.09) 0 1px, transparent 1px 4px), linear-gradient(135deg, #f2e9d8, #e5dac3)",
    description:
      "A thin sheet of wood or plant fibres used for printing, packaging and hygiene products. Fibre source and bleaching affect its footprint.",
    tradeoff:
      "In this demo, paper has moderate impacts and recycles well, but fibres shorten each cycle and coatings or food residue can stop it being recovered.",
    tips: [
      "Look for recycled or certified fibre sources.",
      "Avoid plastic coatings and laminated finishes.",
      "Use only as much paper as the job requires.",
    ],
  },
  {
    id: "cardboard",
    name: "Cardboard",
    family: "Fibre",
    group: "fibres",
    scores: { carbon: 32, recyclability: 81, energy: 38 },
    texture:
      "repeating-linear-gradient(90deg, rgba(90,60,30,.25) 0 2px, transparent 2px 6px), linear-gradient(135deg, #b68c60, #9a7148)",
    description:
      "Thick paperboard, often corrugated, used for boxes and protective packaging. Commonly made with high recycled content.",
    tradeoff:
      "In this demo, cardboard is one of the better options for packaging, but oversized boxes and wet or greasy board reduce the benefit.",
    tips: [
      "Right-size boxes to reduce material and empty space.",
      "Use paper tape instead of plastic tape.",
      "Keep board dry and clean so it can be recycled.",
    ],
  },
  {
    id: "leather",
    name: "Leather",
    family: "Animal-based",
    group: "other",
    scores: { carbon: 83, recyclability: 18, energy: 62 },
    texture:
      "radial-gradient(rgba(0,0,0,.18) 1px, transparent 1.6px) 0 0 / 4px 4px, linear-gradient(135deg, #9b4b2b, #7a3418)",
    description:
      "Tanned animal hide used for shoes, bags, furniture and car interiors. Farming and tanning drive most of its impact.",
    tradeoff:
      "In this demo, leather can last for decades with care, but its upstream impact is high and tanned leather is very difficult to recycle.",
    tips: [
      "Ask how the leather was tanned and where it came from.",
      "Choose products designed to be repaired.",
      "Keep products in use for as long as possible.",
    ],
  },
  {
    id: "copper",
    name: "Copper",
    family: "Metal",
    group: "metals",
    scores: { carbon: 69, recyclability: 91, energy: 80 },
    texture:
      "radial-gradient(circle at 30% 30%, rgba(255,210,170,.45), transparent 50%), linear-gradient(135deg, #c96b3d, #a14b26 60%, #b85a30)",
    description:
      "A highly conductive metal used in wiring, pipes, motors and electronics. Mining and refining ore is energy-intensive.",
    tradeoff:
      "In this demo, copper has a heavy production footprint but keeps its value and properties when recycled, so recovery from cables and devices is key.",
    tips: [
      "Ask for recycled copper where performance allows.",
      "Make wiring and coils easy to remove at end of life.",
      "Avoid bonding copper to other materials.",
    ],
  },
  {
    id: "brick",
    name: "Brick",
    family: "Mineral",
    group: "minerals",
    scores: { carbon: 56, recyclability: 55, energy: 64 },
    texture:
      "radial-gradient(rgba(90,30,10,.35) 1px, transparent 1.8px) 0 0 / 5px 5px, linear-gradient(135deg, #c1633b, #9d4826)",
    description:
      "Fired clay blocks used for walls, paving and facades. Kiln firing is the main source of energy use.",
    tradeoff:
      "In this demo, bricks are very durable and can be reclaimed, but cement mortar often makes clean separation and reuse difficult.",
    tips: [
      "Consider reclaimed bricks where available.",
      "Use lime mortar to allow future reuse.",
      "Source locally to limit transport of heavy units.",
    ],
  },
  {
    id: "rubber",
    name: "Rubber",
    family: "Elastomer",
    group: "polymers",
    scores: { carbon: 61, recyclability: 36, energy: 58 },
    texture:
      "radial-gradient(rgba(255,255,255,.08) 1px, transparent 1.6px) 0 0 / 4px 4px, linear-gradient(135deg, #2f2f2f, #1c1c1c)",
    description:
      "An elastic material from natural latex or synthetic polymers, used for tyres, seals, flooring and footwear.",
    tradeoff:
      "In this demo, rubber is long-lasting, but vulcanised rubber cannot be melted down again, so it is mostly ground into crumb or burned for energy.",
    tips: [
      "Check whether the rubber is natural or synthetic.",
      "Choose replaceable seals and soles over bonded ones.",
      "Look for products using recycled crumb rubber.",
    ],
  },
  {
    id: "cotton",
    name: "Cotton fabric",
    family: "Textile",
    group: "fibres",
    scores: { carbon: 48, recyclability: 46, energy: 51 },
    texture:
      "repeating-linear-gradient(0deg, rgba(120,100,70,.16) 0 1px, transparent 1px 3px), repeating-linear-gradient(90deg, rgba(120,100,70,.16) 0 1px, transparent 1px 3px), linear-gradient(#ddd2bf, #cdc1ab)",
    description:
      "A natural plant fibre woven into clothing, towels and furnishings. Growing it can require a lot of water and agrochemicals.",
    tradeoff:
      "In this demo, cotton is renewable and biodegradable, but water use is high and blended fabrics are hard to recycle back into new fibre.",
    tips: [
      "Look for organic or responsibly grown cotton.",
      "Avoid blends if fibre-to-fibre recycling matters.",
      "Wash cooler and less often to extend garment life.",
    ],
  },
  {
    id: "polyester",
    name: "Polyester fabric",
    family: "Textile",
    group: "fibres",
    scores: { carbon: 70, recyclability: 33, energy: 77 },
    texture:
      "repeating-linear-gradient(45deg, rgba(255,255,255,.09) 0 1px, transparent 1px 3px), radial-gradient(circle at 40% 40%, #5283b8, #2a5385)",
    description:
      "A synthetic, fossil-based fibre used in clothing, upholstery and outdoor gear. Durable, quick-drying and inexpensive.",
    tradeoff:
      "In this demo, polyester is durable but fossil-based, sheds microfibres when washed, and is rarely recycled back into textiles.",
    tips: [
      "Prefer recycled polyester where available.",
      "Avoid blends with natural fibres.",
      "Choose durable items you will keep for longer.",
    ],
  },
  {
    id: "pvc",
    name: "PVC",
    family: "Polymer",
    group: "polymers",
    scores: { carbon: 75, recyclability: 22, energy: 69 },
    texture:
      "linear-gradient(180deg, rgba(255,255,255,.5), transparent 45%), linear-gradient(135deg, #bfbfbf, #999999)",
    description:
      "Polyvinyl chloride, a rigid or flexible plastic used for pipes, window frames, flooring and cables.",
    tradeoff:
      "In this demo, PVC is long-lasting in buildings, but additives and chlorine content make recycling and safe disposal more complicated.",
    tips: [
      "Check for alternatives in pipes, flooring and packaging.",
      "Ask about additives such as plasticisers.",
      "Use take-back schemes for offcuts and old products.",
    ],
  },
  {
    id: "wood",
    name: "Wood",
    family: "Plant-based",
    group: "other",
    scores: { carbon: 24, recyclability: 64, energy: 28 },
    texture:
      "repeating-linear-gradient(100deg, rgba(120,70,20,.22) 0 2px, transparent 2px 9px), linear-gradient(135deg, #da9b4f, #b9772f)",
    description:
      "A versatile natural material used in structures, interiors and everyday products. Species, sourcing and finishes change its impact.",
    tradeoff:
      "In this demo, wood has lower carbon and energy scores, but recovery is not guaranteed. Coatings, adhesives and local collection can limit recycling.",
    tips: [
      "Check species, origin and responsible sourcing.",
      "Design for repair, reuse and disassembly.",
      "Confirm local recovery options for treated wood.",
    ],
  },
  {
    id: "clay",
    name: "Clay",
    family: "Mineral",
    group: "minerals",
    scores: { carbon: 38, recyclability: 52, energy: 47 },
    texture:
      "radial-gradient(rgba(140,90,60,.3) 1px, transparent 1.8px) 0 0 / 6px 6px, linear-gradient(135deg, #e4ba9b, #cf9f80)",
    description:
      "A natural earth material shaped into pottery, tiles and plasters. Unfired clay can return to the ground; fired clay becomes ceramic.",
    tradeoff:
      "In this demo, raw clay has a low footprint, but firing adds energy and fired ceramics cannot easily be turned back into clay.",
    tips: [
      "Consider unfired clay plasters for interiors.",
      "Source locally to reduce transport.",
      "Choose durable glazes to extend product life.",
    ],
  },
];
