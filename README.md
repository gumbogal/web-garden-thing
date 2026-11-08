# Web Garden Thing

# 🌿 Web Garden Thing

**A procedural botanical world inspired by British temperate woodland.**

Web Garden Thing is a procedural 3D modelling project exploring the creation of stylised, low-poly botanical assets using Python and Blender.

Inspired by the native flora of Britain and north-western Europe, the project aims to develop a diverse digital collection of plants before eventually bringing them together into an interactive, procedurally populated natural environment.

The project combines botanical research, procedural modelling and environmental design. Its central ambition is to create a digital woodland that feels botanically diverse and recognisable while maintaining a distinctive, cohesive visual identity.

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

### 2. Natural variation

Develop systems for introducing controlled randomness into generated models.

Repeated generations of the same species should produce recognisably related but individually different plants.

Variation should be biologically plausible rather than arbitrary.

### 3. Ecological diversity

Expand the collection to represent different vegetation layers and ecological niches.

The system should eventually be capable of generating complementary groups of plants that could plausibly coexist within a British woodland.

### 4. Seasonal development

Introduce seasonal states and different growth stages.

Potential features include:

- Spring flowering.
- Summer foliage.
- Autumn leaf colour and leaf loss.
- Winter dormancy.
- Different stages of plant maturity.

### 5. Procedural environments

Use the generated assets to construct larger natural environments.

This could include woodland floors, clearings, hedgerows and other representative British habitats.

Plant distribution should eventually take environmental conditions into account rather than relying entirely on random placement.

### 6. Interactive web experience

My longer-term ambition is to bring the botanical collection into an interactive digital environment.

Potential features include:

- Exploring a procedurally populated woodland.
- Inspecting individual plants.
- Viewing botanical information about each species.
- Generating different woodland compositions.
- Experiencing seasonal changes.

The eventual rendering technology and implementation can be decided as the asset library develops.

---

## 🗺️ Development roadmap

I intend to develop the project incrementally, prioritising a reliable procedural generation pipeline before expanding into increasingly complex botanical systems.

| Phase | Goal                                                   | Estimated duration |
| ----- | ------------------------------------------------------ | ------------------ |
| 1     | Development environment and Blender scripting workflow | 1 week             |
| 2     | Core procedural plant generation system                | 1–2 weeks          |
| 3     | Initial British woodland species catalogue             | 3–5 weeks          |
| 4     | Botanical accuracy and natural variation               | 3–5 weeks          |
| 5     | Additional plant structures, flowers and fruits        | 3–4 weeks          |
| 6     | Seasonal variation and growth stages                   | 2–4 weeks          |
| 7     | Woodland composition and ecological distribution       | 3–5 weeks          |
| 8     | Asset optimisation and export pipeline                 | 2–3 weeks          |
| 9     | Interactive environment and web integration            | 4–8 weeks          |

_Estimates are indicative and assume steady development. Phases may overlap, and botanical research or technical challenges may extend the schedule._

### Milestones

- [x] Establish a reliable VS Code and Blender workflow.
- [ ] Develop reusable procedural modelling functions.
- [ ] Generate a first collection of representative woodland plants.
- [ ] Establish a consistent low-poly visual style.
- [ ] Expand the collection across different botanical growth forms.
- [ ] Introduce controlled species-specific variation.
- [ ] Improve botanical accuracy through research and iteration.
- [ ] Implement seasonal and developmental variation.
- [ ] Develop systems for ecological plant distribution.
- [ ] Create complete woodland environments.
- [ ] Prepare assets for interactive use.
- [ ] Develop the eventual web-based experience.

---

## 🛠️ Technology

The project currently uses the following technologies:

| Technology          | Purpose                                                        |
| ------------------- | -------------------------------------------------------------- |
| Python              | Procedural generation and automation                           |
| Blender 5.2.3 LTS   | 3D modelling, scene management and rendering                   |
| `bpy`               | Blender's Python API                                           |
| VS Code             | Primary script editor and development environment              |
| Blender Development | VS Code extension for Blender integration and script execution |
| Pylance             | Python language intelligence                                   |
| `fake-bpy-module`   | Blender API type information for VS Code                       |
| `uv`                | Python environment and dependency management                   |
| Git                 | Version control                                                |

Blender is responsible for executing the actual modelling operations. The external Python environment is primarily for development tooling, code analysis and editor support.

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
- **Python 3.8 or later:** Required for the development tooling described below.
- **uv:** Python package and virtual environment manager.
- **Pylance:** Python language intelligence and diagnostics for VS Code.
- **Blender Development:** VS Code extension for interacting with Blender and executing scripts.
- **Git:** Recommended for version control.

You do not need to install Python, `bpy`, `uv` or any VS Code extensions if you simply want to execute the scripts through Blender's built-in Scripting workspace.

### 1. Obtain the project

Clone the repository or download its contents.

Open the project directory in VS Code or Blender, depending on your intended use.

The directory should contain files similar to:

```text
web-garden-thing/
├── .venv/
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
├── web_garden.blend
└── ...
```

The `.blend` file contains the Blender scene, while the Python scripts contain the procedural generation logic.

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

To explicitly select a Python interpreter:

```bash
uv venv --python 3.15
uv sync
```

The current development setup uses Homebrew Python 3.15.2, although this particular installation method is not required.

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

For this project, the dependency is recorded in `pyproject.toml` under the development dependency group.

If setting up the project from scratch, you can add it using:

```bash
uv add --dev fake-bpy-module
```

This adds the dependency to `pyproject.toml` and updates `uv.lock`.

Then run:

```bash
uv sync
```

If the project already contains the dependency and lockfile, simply running `uv sync` is sufficient.

**Installing manually with pip**

If you are not using `uv`, activate your virtual environment and install the package with:

```bash
python -m pip install fake-bpy-module
```

For a Blender-version-specific package, the alternative is:

```bash
python -m pip install fake-bpy-module-5.2
```

The general package provides the latest generated API definitions, while the version-specific package targets Blender 5.2.

For more information, see the [fake-bpy-module project on PyPI](https://pypi.org/project/fake-bpy-module/).

### 5. Configure VS Code

Open the project directory in VS Code.

Install the following extensions through the VS Code Extensions Marketplace:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Blender Development](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development)

The Blender Development extension is particularly useful because it provides Blender integration directly within VS Code, including commands for starting Blender sessions and executing scripts.

Once installed:

1. Open the project directory in VS Code.
2. Select the Python interpreter inside `.venv`.
3. Open the Command Palette.
4. Use the available Blender Development commands to configure and start Blender.
5. Select your Blender executable when prompted.

The extension provides commands such as:

- `Blender: Start`
- `Blender: Run Script`
- `Blender: Reload Addons`

The exact commands available depend on the extension's configuration and project type.

### 6. Configure Blender API support

Even with `fake-bpy-module` installed, VS Code may need to know where Blender's own Python modules are located.

The project uses VS Code's `python.analysis.extraPaths` setting to provide this information.

For my current Blender 5.2.3 installation, the path is:

```text
/Applications/Blender.app/Contents/Resources/5.2/scripts/modules
```

To configure this:

1. Open VS Code settings.
2. Open the project's `settings.json`.
3. Add the Blender modules directory to `python.analysis.extraPaths`.

For example:

```json
{
  "python.analysis.extraPaths": [
    "/Applications/Blender.app/Contents/Resources/5.2/scripts/modules"
  ]
}
```

This path is specific to my macOS installation. On Windows and Linux, use the equivalent `scripts/modules` directory within the Blender installation.

The combination of `fake-bpy-module` and Blender's own module paths gives Pylance the information it needs to understand Blender's Python API.

### 7. My VS Code and Blender workflow

My preferred workflow is to use VS Code for all script editing and Blender for execution and visual inspection.

The important thing is that Blender should not need to be relaunched every time a script changes.

My workflow is:

1. Open the project directory in VS Code.
2. Start Blender through the Blender Development extension.
3. Keep that Blender session running.
4. Edit the relevant Python script in VS Code.
5. Save the changes.
6. Use `Blender: Run Script` to execute the saved script in the Blender session.
7. Inspect the generated geometry in Blender.
8. Return to VS Code, make adjustments and repeat.

The extension handles the communication between VS Code and Blender, avoiding the need to repeatedly launch Blender through separate terminal commands or create additional Blender processes for each execution.

**The distinction is important:** VS Code is responsible for editing and managing the code, while Blender's own Python runtime executes it.

### 8. Iterating on generated models

Procedural modelling is an iterative process.

Rather than manually modifying generated geometry, changes should generally be made to the Python generation logic.

This keeps the results reproducible and allows improvements to benefit subsequent generations.

When rerunning scripts, take care to manage previously generated objects so repeated executions do not leave unwanted duplicates in the scene.

---

## 🌱 Project philosophy

My central principle for Web Garden Thing is that **botanical diversity should inform procedural generation, rather than procedural generation dictating botanical diversity**.

I don't want to create an arbitrary collection of attractive plants. I want to explore how computational modelling can represent the extraordinary variety of real botanical life, while interpreting it through a distinctive low-poly visual style.

That means researching the organisms being modelled, understanding their defining characteristics and translating those characteristics into reusable procedural systems.

The British woodland biome provides a coherent ecological foundation for this exploration, while leaving plenty of room to expand into other habitats in the future.

Ultimately, I want to create a living digital botanical collection: varied, recognisable, ecologically informed and visually cohesive, capable of growing alongside the project itself.

---

_Web Garden Thing is an evolving project. Its botanical catalogue, technical implementation and eventual interactive features will develop as the procedural modelling system matures._
