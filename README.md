# Real Estate (`estate`) - Odoo 17 learning project

> **Note:** This is a **learning project**. I'm a beginner learning Odoo
> development, and I'm building this module step by step to practice. It is
> **not production-ready**, and some parts of it exist only so I can
> practice a specific Odoo concept (see
> [Models used for learning](#models-used-for-learning-not-core)).
> Feedback and suggestions are very welcome.

## What it does

A small module to manage real estate properties:

- Create properties with price, bedrooms, living area, facades, garage and
  garden information.
- Every property gets an automatic reference number (`PRT00001`, `PRT00002`, ...)
  from an `ir.sequence`.
- A simple workflow: **Draft -> Pending -> Sold -> Closed** (you can also go
  back to Draft from Pending or Sold), driven by buttons in the form view
  (and by server actions from the list view).
- Every state change is saved in a **history log** (who changed it, from which
  state to which state).
- A computed field shows the difference between the expected and the
  selling price, and a warning appears if the expected price is lower than the
  selling price.
- A daily scheduled action (cron) flags properties whose expected selling date
  has passed and that are not sold or closed. They are shown in red in the
  list view.
- Tags, owners and a PDF report for each property.
- Chatter (messages and activities) on properties.

## Requirements

- Odoo **17.0**
- Odoo modules: `sale_management`, `mail`

## Installation

1. Clone this repository into a folder that is in your `addons_path`.
   The folder **must** be named `estate`, because that is the technical
   name of the module:
   ```bash
   cd /path/to/your/custom_addons
   git clone https://github.com/mina77remon-prog/estate.git
   ```
2. Restart Odoo and update the apps list, then install **Real Estate**.
   Or from the command line:
   ```bash
   ./odoo-bin -c odoo.conf -d <your_database> -i estate
   ```
3. Go to **Settings -> Users**, open your user and, in the *Real Estate*
   section, choose **Property Manager** (or **Property User**).
   Without one of these groups you won't see the Real Estate data.
   The default `admin` user is added to the Manager group automatically.

## Security

| Group | What it can do |
|---|---|
| **Property User** | Sees and edits only the properties they created. Cannot delete properties. |
| **Property Manager** | Sees all properties, has full access, and can use the *Configuration* menu (owners and tags). |

The Manager group includes the User group.

## Models

### Core models

| Model | Purpose |
|---|---|
| `estate.property` | The main model: a property and its workflow. |
| `estate.property.line` | Rows of the "Bedrooms" tab (description and area). |
| `estate.owner` | The owner of a property. |
| `estate.tag` | Tags that can be attached to properties (many-to-many). |
| `estate.property.history` | Read-only log of state changes. |

### Models used for learning (not core)

These are here because I'm practicing Odoo concepts. The module works
without them, and they may be changed or removed later.

| Model | What I'm practicing |
|---|---|
| `estate.building` | A simple model with chatter (`mail.thread`), `_rec_name` and archiving. It is linked to properties through the `building_id` field, but it is still very basic. |
| `estate.client` | **Prototype inheritance** (`_name` + `_inherit`). It is a copy of `estate.owner` and is **not used anywhere yet**. |
| `res.partner` (extended) | Extending an existing model with a stored computed field and view inheritance. |
| `sale.order` (extended) | Extending an existing model and overriding `action_confirm`. At the moment the override only writes a log line. |

## Project structure

```
estate/
├── __manifest__.py
├── data/          # sequence
├── models/        # one file per model
├── reports/       # PDF report (QWeb)
├── security/      # groups, record rules, access rights
├── static/        # icon and CSS
└── views/         # views, actions and menus
```

## Known limitations

- No automated tests yet.
- No demo data.
- Some of the code is intentionally simple because I'm still learning.
- `estate.client` is not used in any view.
- The workflow is only enforced by the form buttons; the server actions in the
  list view can move a property to any state.
- Duplicating a property fails because `name` has a unique constraint.
- The PDF report is a simple first version (basic layout).

## What I'm working on / learning next

- Writing tests for the main model.
- Improving the workflow code and the views.
- Connecting the learning models to the rest of the module in a meaningful way.

## Feedback

If you notice something that could be done better, please open an issue or a
pull request. I'm happy to learn from it.

## License

This project is licensed under the **GNU Lesser General Public License v3.0
(LGPL-3.0)**. See the [LICENSE](LICENSE) file for the full text.
