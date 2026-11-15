# 🌿 Web Garden Thing

**A procedural botanical world inspired by British temperate woodland.**

Web Garden Thing is a procedural 3D modelling project exploring the creation of stylised, low-poly botanical assets using Python and Blender.

Inspired by the native flora of Britain and north-western Europe, the project aims to develop a diverse digital collection of plants before eventually bringing them together into an interactive, procedurally populated natural environment.

The project combines botanical research, database design, procedural modelling and environmental design. Its central ambition is to create a digital woodland that feels botanically diverse and recognisable while maintaining a distinctive, cohesive visual identity.

---

## 🎨 Visual direction: Stylised low-poly

A defining characteristic of Web Garden Thing is its intended **low-poly aesthetic**.

Rather than pursuing photorealism, I want to create stylised botanical models that capture the essential character and silhouette of real plants through relatively simple geometry.

The aesthetic should balance botanical recognisability with artistic interpretation.

Some guiding principles include:

- **Simplified geometry:** Use carefully considered polygon counts rather than unnecessarily complex meshes.
- **Distinctive silhouettes:** Preserve the characteristic shapes and growth habits of individual species.
- **Stylised foliage:** Represent leaves using simplified geometry while retaining recognisable leaf shapes and arrangements.
- **Faceted surfaces:** Allow polygonal geometry and flat shading to contribute to the visual character.
- **Cohesive proportions:** Maintain a consistent visual language across different species.
- **Natural variation:** Avoid overly symmetrical or mechanically repetitive models.
- **Thoughtful colour palettes:** Use natural, slightly stylised colours that work together across the environment.

The intention is not to make every plant look identical in style, but to ensure that trees, shrubs, ferns, grasses and flowering plants feel as though they belong to the same world.

---

## 🌳 The biome: British temperate woodland

The initial botanical reference is **British temperate woodland**, with a broader focus on native species found throughout Britain and north-western Europe.

Woodland offers an especially interesting starting point because of its extraordinary diversity of plant forms, from towering canopy trees to delicate ground-covering flowers.

Rather than generating generic vegetation, I want the species catalogue to reflect the botanical character of a real ecosystem.

### Ecological characteristics

Several characteristics will influence the modelling and eventual environmental generation:

- **Layered vegetation:** Woodland contains distinct layers, including the canopy, understory, shrub layer and ground flora.
- **Seasonality:** Plants change throughout the year, from spring flowering to summer growth, autumn colour and winter dormancy.
- **Natural variation:** Individual plants of the same species differ in size, proportions, branching and foliage.
- **Ecological relationships:** Species occupy different niches depending on light, soil, moisture and competition.
- **Native diversity:** Species selection should reflect the character of British and north-western European woodland.

### Representative species

The eventual catalogue should encompass a broad range of native plants and growth forms.

| Category           | Representative species                           |
| ------------------ | ------------------------------------------------ |
| Canopy trees       | English oak, silver birch, European beech, rowan |
| Smaller trees      | Hazel, hawthorn, holly                           |
| Shrubs             | Elder, guelder rose, spindle                     |
| Climbing plants    | Common ivy, honeysuckle                          |
| Ferns              | Male fern, lady fern, bracken                    |
| Flowering plants   | Bluebell, wood anemone, primrose, foxglove       |
| Ground cover       | Wood sorrel, lesser celandine, wild garlic       |
| Grasses and sedges | Wood melick, wood sedge                          |
| Mosses             | Common woodland mosses                           |

This is an illustrative selection rather than a definitive species list. I intend to expand the catalogue through botanical research, prioritising native species and representative diversity.

---

## 🎯 Long-term goals

The project is intended to develop beyond simply generating individual plant meshes.

### 1. Procedural botanical asset library

Create a growing collection of procedurally generated plants, each representing a recognisable species.

Models should capture defining characteristics, including:

- Leaf shape, arrangement and venation.
- Branching patterns and growth habits.
- Stem and trunk proportions.
- Flower and fruit structures.
- Species-specific silhouettes.
- Natural asymmetry and variation.

### 2. Botanical database

Develop a structured botanical database using SQLite.

Rather than embedding species information directly into individual generation scripts, I want to maintain a central source of botanical information that can be accessed by the Python application.

The database will eventually contain:

- Scientific names and taxonomic classifications.
- Common names and alternative names.
- Plant growth habits and morphological characteristics.
- Habitat preferences and ecological associations.
- Seasonal characteristics.
- References and sources supporting individual records.

An important consideration is maintaining the provenance of botanical information. Researched characteristics should be distinguishable from approximations or creative decisions made by the procedural generation system.

### 3. Natural variation

Develop systems for introducing controlled randomness into generated models.

Repeated generations of the same species should produce recognisably related but individually different plants.

Variation should be biologically plausible rather than arbitrary.

### 4. Ecological diversity

Expand the collection to represent different vegetation layers and ecological niches.

The system should eventually be capable of generating complementary groups of plants that could plausibly coexist within a British woodland.

### 5. Seasonal development

Introduce seasonal states and different growth stages.

Potential features include:

- Spring flowering.
- Summer foliage.
- Autumn leaf colour and leaf loss.
- Winter dormancy.
- Different stages of plant maturity.

### 6. Procedural environments

Use the generated assets to construct larger natural environments.

This could include woodland floors, clearings, hedgerows and other representative British habitats.

Plant distribution should eventually take environmental conditions into account rather than relying entirely on random placement.

### 7. Interactive web experience

My longer-term ambition is to bring the botanical collection into an interactive digital environment.

Potential features include:

- Exploring a procedurally populated woodland.
- Inspecting individual plants.
- Viewing botanical information about each species.
- Generating different woodland compositions.
- Exploring plant habitats and ecological relationships.
- Experiencing seasonal changes.

The eventual rendering technology and implementation can be decided as the asset library develops.

---

## 🗄️ Botanical database and SQLite

SQLite will provide the project's central botanical data store.

The intention is to separate botanical information from the procedural modelling implementation. This means the same species data could eventually be used by the Blender generation scripts, asset management tools and interactive web experience.

SQLite is particularly suitable for this project because it provides a lightweight relational database without requiring a separate database server.

### Database structure

The initial database design uses several related tables.

| Table              | Purpose                                                    |
| ------------------ | ---------------------------------------------------------- |
| `taxa`             | Taxonomic classifications and relationships                |
| `species`          | Individual species records and botanical characteristics   |
| `common_names`     | Common and alternative names for species                   |
| `habitats`         | Definitions of different habitat types                     |
| `species_habitats` | Relationships between species and their habitats           |
| `sources`          | References and sources used for botanical research         |
| `species_sources`  | Links between species records and their supporting sources |

The structure is intended to avoid unnecessary duplication and allow botanical information to be expanded without having to modify the procedural generation code.

For example, a species may have multiple common names, inhabit multiple habitat types and be supported by several references.

These relationships are represented through separate tables rather than storing everything in a single species record.

### Botanical data and procedural parameters

An important distinction is that not every value used to generate a plant is necessarily a documented botanical fact.

I intend to keep two categories of information conceptually separate:

**Botanical information**

- Scientific and common names.
- Taxonomic classification.
- Documented leaf arrangements.
- Growth habits.
- Habitat preferences.
- Flowering periods.
- Supporting references.

**Procedural modelling parameters**

- Generated plant height.
- Branch distribution.
- Leaf dimensions.
- Geometry density.
- Random variation ranges.
- Model-specific visual adjustments.

The first category describes the plant. The second describes how the plant is represented in 3D.

Some procedural parameters may be informed by botanical measurements, but they should not automatically be treated as scientifically documented values.

### Python database access

The database will be accessed through a dedicated Python data-access layer.

Rather than allowing individual Blender generation scripts to contain their own SQL queries, the application should provide reusable functions for retrieving species information.

For example:

```python
species = get_species("quercus_petraea")
```

This would retrieve the relevant species record and its associated information from SQLite.

The generation system could then use that information to determine which characteristics should influence the resulting model.

This separation should make the project easier to maintain and allow the database implementation to evolve without requiring major changes to the Blender generation scripts.

### Data quality and provenance

Botanical accuracy is an important consideration.

I intend to use reliable botanical references when populating the database and retain source information alongside the relevant records.

This will make it possible to distinguish between:

- Information supported by botanical references.
- Information inferred from other documented characteristics.
- Procedural approximations.
- Artistic decisions made to achieve the intended low-poly aesthetic.

The database should provide a foundation for informed modelling rather than create a false impression of scientific precision.

---

## 🗺️ Development roadmap

I intend to develop the project incrementally, prioritising a reliable procedural generation pipeline before expanding into increasingly complex botanical systems.

| Phase | Goal                                                   | Estimated duration |
| ----- | ------------------------------------------------------ | ------------------ |
| 1     | Development environment and Blender scripting workflow | 1 week             |
| 2     | SQLite database structure and Python data-access layer | 1–2 weeks          |
| 3     | Botanical research and initial database population     | 2–4 weeks          |
| 4     | Core procedural plant generation system                | 2–3 weeks          |
| 5     | Initial British woodland species catalogue             | 3–5 weeks          |
| 6     | Botanical accuracy and natural variation               | 3–5 weeks          |
| 7     | Additional plant structures, flowers and fruits        | 3–4 weeks          |
| 8     | Seasonal variation and growth stages                   | 2–4 weeks          |
| 9     | Woodland composition and ecological distribution       | 3–5 weeks          |
| 10    | Asset optimisation and export pipeline                 | 2–3 weeks          |
| 11    | Interactive environment and web integration            | 4–8 weeks          |

_Estimates are indicative and assume steady development. Phases may overlap, and botanical research or technical challenges may extend the schedule._

### Milestones

- [x] Establish a reliable VS Code and Blender workflow.
- [x] Begin developing the SQLite database structure.
- [x] Establish an initial relational data model.
- [ ] Complete and validate the Python database-access layer.
- [ ] Populate the database with researched botanical information.
- [ ] Develop reusable procedural modelling functions.
- [ ] Generate a first collection of representative woodland plants.
- [ ] Establish a consistent low-poly visual style.
- [ ] Expand the collection across different botanical growth forms.
- [ ] Introduce controlled species-specific variation.
- [ ] Improve botanical accuracy through research and iteration.
- [ ] Implement seasonal and developmental variation.
- [ ] Develop systems for ecological plant distribution.
- [ ] Create complete woodland environments.
- [ ] Prepare optimised assets for interactive use.
- [ ] Develop the eventual web-based experience.

---

## 🔄 Planned end-to-end workflow

The eventual project architecture is intended to follow a pipeline in which botanical research, structured data, procedural generation and interactive presentation are separate but connected stages.

<text>**1. Botanical research**</text>

Identify a species and collect relevant botanical information from reliable references.

↓

<text>**2. Database population**</text>

Record the species, taxonomy, common names, habitats, characteristics and supporting sources in SQLite.

↓

<text>**3. Python data access**</text>

Retrieve species information through the Python data-access layer, validate the available information and prepare it for generation.

↓

<text>**4. Procedural generation in Blender**</text>

Pass the relevant botanical characteristics into reusable generation functions. Blender uses these parameters to construct a stylised, low-poly representation of the plant.

↓

<text>**5. Asset refinement and optimisation**</text>

Inspect the generated model, adjust its procedural parameters, establish appropriate levels of detail and prepare it for export.

↓

<text>**6. Asset export**</text>

Export the resulting models in a web-compatible format, with glTF/GLB as the intended target.

↓

<text>**7. Interactive web environment**</text>

Load the exported assets into the eventual web experience and use the botanical database to provide relevant species information and ecological context.

### Architecture overview

The intended separation of responsibilities looks something like this:

```text
             BOTANICAL RESEARCH
                     |
                     v
              SQLITE DATABASE
                     |
                     v
             PYTHON DATA LAYER
                     |
                     v
           PROCEDURAL GENERATION
                     |
                     v
                  BLENDER
                     |
                     v
            ASSET OPTIMISATION
                     |
                     v
               GLB / GLTF
                     |
                     v
             WEB ENVIRONMENT
                     |
              +------+------+
              |             |
              v             v
         3D PLANTS    BOTANICAL DATA
```

The database and 3D asset pipeline are deliberately separate. The web experience should not need to understand how a plant was procedurally generated in Blender.

Likewise, Blender should not need to know how botanical information was originally researched or collected. It should receive structured data through the Python layer.

This separation should make it possible to improve individual parts of the project without having to redesign the entire system.

---

## 🛠️ Technology

The project currently uses the following technologies:

| Technology          | Purpose                                                        |
| ------------------- | -------------------------------------------------------------- |
| Python              | Procedural generation, database access and automation          |
| Blender 5.2.3 LTS   | 3D modelling, scene management and rendering                   |
| `bpy`               | Blender's Python API                                           |
| SQLite              | Botanical information and relational data storage              |
| VS Code             | Primary script editor and development environment              |
| Blender Development | VS Code extension for Blender integration and script execution |
| Pylance             | Python language intelligence                                   |
| `fake-bpy-module`   | Blender API type information for VS Code                       |
| `uv`                | Python environment and dependency management                   |
| Git                 | Version control                                                |
| glTF / GLB          | Intended 3D asset export formats                               |
| Three.js            | Potential web-based 3D rendering technology                    |

Blender is responsible for executing the actual modelling operations. The external Python environment is primarily for development tooling, code analysis and editor support.

SQLite is intended to be accessible independently of Blender through the Python data-access layer.

---

## 💻 Installation and usage

There are two ways to interact with the project:

1. **Using the generator:** Open the Blender project and execute its Python scripts.
2. **Developing the generator:** Edit the Python scripts using an editor such as VS Code and execute them in Blender.

The project does not require a particular operating system. Blender is available for Windows, macOS and Linux.

### Requirements

**Essential**

- **Blender 5.2.3 LTS:** Required to open the project and execute the procedural generation scripts. Download from [blender.org](https://www.blender.org/download/).
- **Project files:** Including the Python generation scripts and, where provided, the `.blend` project file.

**Recommended for development**

- **Visual Studio Code:** Primary code editor.
- **Python:** Required for the external development environment and database tooling.
- **uv:** Python package and virtual environment manager.
- **Pylance:** Python language intelligence and diagnostics for VS Code.
- **Blender Development:** VS Code extension for interacting with Blender and executing scripts.
- **Git:** Recommended for version control.

SQLite is included in Python's standard library, so a separate SQLite installation is not normally necessary for Python database access.

You do not need to install Python, `bpy`, `uv` or any VS Code extensions if you simply want to execute the scripts through Blender's built-in Scripting workspace.

### 1. Obtain the project

Clone the repository or download its contents.

Open the project directory in Blender or VS Code, depending on your intended use.

The directory should contain files similar to:

```text
web-garden-thing/
├── .venv/
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
├── web_garden.blend
├── data/
└── src/
    └── web_garden_thing/
        └── ...
```

The `.blend` file contains the Blender scene, the `data` directory is intended for project data such as the SQLite database, and the Python package contains the application logic.

### 2. Running scripts directly in Blender

This is the simplest way to use the project without setting up a development environment.

1. Install Blender 5.2.3 LTS.
2. Open Blender.
3. Open `web_garden.blend`, if you want to use the supplied project scene.
4. Navigate to Blender's **Scripting** workspace.
5. Open the relevant Python generation script using the Text Editor's Open option.
6. Press **Run Script** in the Text Editor.
7. Inspect the generated geometry in the 3D Viewport.

Blender executes the script using its own bundled Python environment, which includes the `bpy` API.

You do not need to install `bpy` separately or activate a Python virtual environment.

### 3. Setting up the Python development environment

For development, I use `uv` to manage a local Python virtual environment and its dependencies.

Install `uv` following the instructions at [docs.astral.sh/uv](https://docs.astral.sh/uv/).

Once installed, open a terminal in the project directory.

The project uses `pyproject.toml` to define its development dependencies and `uv.lock` to record their resolved versions.

Run:

```bash
uv sync
```

This creates the project's `.venv` environment if necessary and installs the dependencies recorded in the lockfile.

To activate the environment manually:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

Alternatively, commands can be run through `uv` without manually activating the environment.

### 4. Installing fake-bpy-module

`fake-bpy-module` provides Python type information and API definitions for Blender.

This allows Pylance to recognise Blender-specific modules, such as `bpy`, and provide code completion, diagnostics and navigation.

It is important to understand that this is an editor aid. It does not provide a functioning Blender runtime or allow Blender geometry to be generated independently of Blender.

The dependency is managed through `pyproject.toml`.

To add it:

```bash
uv add --dev fake-bpy-module
```

This adds the dependency to `pyproject.toml` and updates `uv.lock`.

Then run:

```bash
uv sync
```

If the project already contains the dependency and lockfile, simply running `uv sync` is sufficient.

For more information, see the [fake-bpy-module project on PyPI](https://pypi.org/project/fake-bpy-module/).

### 5. Configure VS Code

Open the project directory in VS Code.

Install the following extensions:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Blender Development](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development)

The Blender Development extension provides Blender integration directly within VS Code, including commands for starting Blender sessions and executing scripts.

Once installed:

1. Open the project directory in VS Code.
2. Select the Python interpreter inside `.venv`.
3. Open the Command Palette.
4. Use the Blender Development commands to configure and start Blender.
5. Select your Blender executable when prompted.

### 6. Configure Blender API support

VS Code may need to know where Blender's own Python modules are located.

The project uses VS Code's `python.analysis.extraPaths` setting to provide this information.

For my current Blender 5.2.3 installation, the path is:

```text
/Applications/Blender.app/Contents/Resources/5.2/scripts/modules
```

To configure this, add the equivalent Blender `scripts/modules` directory to the project's VS Code `settings.json`:

```json
{
  "python.analysis.extraPaths": ["/path/to/blender/scripts/modules"]
}
```

The path is installation-specific, so it should be adjusted for Windows, macOS or Linux.

The combination of `fake-bpy-module` and Blender's own module paths gives Pylance the information it needs to understand Blender's Python API.

### 7. My VS Code and Blender workflow

My preferred workflow is to use VS Code for all script editing and Blender for execution and visual inspection.

1. Open the project directory in VS Code.
2. Start Blender through the Blender Development extension.
3. Keep that Blender session running.
4. Edit the relevant Python script in VS Code.
5. Save the changes.
6. Use `Blender: Run Script` to execute the saved script in the Blender session.
7. Inspect the generated geometry in Blender.
8. Return to VS Code, make adjustments and repeat.

The extension handles communication between VS Code and Blender, avoiding the need to repeatedly launch Blender through separate terminal commands or create additional Blender processes for each execution.

**VS Code is responsible for editing and managing the code, while Blender's own Python runtime executes it.**

### 8. Working with the SQLite database

The database is intended to be managed through the project's Python data-access layer.

Rather than writing SQL queries directly inside Blender generation scripts, the application should expose reusable functions for retrieving botanical information.

For example:

```python
species = get_species("quercus_petraea")
```

The returned information can then be passed to the procedural generation system.

SQLite itself does not require a running database server. Python can access the database using its built-in `sqlite3` module.

For direct database inspection, a graphical SQLite browser can also be useful, although this is optional.

### 9. Iterating on generated models

Procedural modelling is an iterative process.

Rather than manually modifying generated geometry, changes should generally be made to the Python generation logic.

This keeps the results reproducible and allows improvements to benefit subsequent generations.

When rerunning scripts, take care to manage previously generated objects so repeated executions do not leave unwanted duplicates in the scene.

---

## 🌱 Project philosophy

My central principle for Web Garden Thing is that **botanical diversity should inform procedural generation, rather than procedural generation dictating botanical diversity**.

I don't want to create an arbitrary collection of attractive plants. I want to explore how computational modelling can represent the extraordinary variety of real botanical life, while interpreting it through a distinctive low-poly visual style.

The SQLite database is an important part of this ambition. It provides a place to preserve botanical knowledge, document sources and build relationships between species and their environments.

That information can then inform procedural generation, allowing the resulting models to be more than visually appealing approximations of generic vegetation.

Ultimately, I want to create a living digital botanical collection: varied, recognisable, ecologically informed and visually cohesive, capable of growing alongside the project itself.

---

_Web Garden Thing is an evolving project. Its botanical catalogue, technical implementation and eventual interactive features will develop as the procedural modelling system matures._
