# Refactoring Plan: `dashboard_app/app.py`

This document outlines a phased refactoring plan to break down the monolithic `dashboard_app/app.py` file into smaller, more manageable modules. The primary goal is to improve maintainability and ease of future development by ensuring each file is under 1000 lines of code.

## 1. Goal

Refactor the `dashboard_app/app.py` file, which currently has over 8,600 lines, into a set of smaller, more focused modules. Each module should have a clear responsibility, and the final `app.py` file should be a lean entry point for the application.

## 2. Strategy

The refactoring will be executed in a series of small, incremental phases to minimize the risk of introducing errors. Each phase will focus on extracting a specific piece of functionality into a new file or module. An aggressive Git policy will be followed, with a commit after each successfully completed phase.

## 3. Proposed File Structure

The following file structure is proposed for the refactored `dashboard_app`:

```
dashboard_app/
├── app.py                  # Main application entry point (slimmed down)
├── layout.py               # Defines the Dash application layout
├── utils.py                # Helper and utility functions
├── callbacks/              # Directory for Dash callbacks
│   ├── __init__.py
│   ├── main_callbacks.py       # Main content update callback
│   ├── graph_callbacks.py      # Callbacks for generating graphs
│   ├── kf_callbacks.py         # Callbacks for the Key Findings feature
│   └── ui_callbacks.py         # Callbacks for UI interactions (modals, language, etc.)
└── ...                     # Existing files
```

## 4. Refactoring Phases

### Phase 1: Layout Extraction

1.  **Create `dashboard_app/layout.py`**.
2.  **Move Layout Components**: Move the definitions of `sidebar`, `header`, `notes_modal`, `key_findings_modal`, `citation_modal`, `app.layout`, and any other layout-specific variables from `app.py` to `layout.py`.
3.  **Update `app.py`**: Import the layout components from `layout.py` and assign them to `app.layout`.
4.  **Review and Commit**:
    *   Run the application to ensure the layout renders correctly.
    *   Commit changes with the message: `refactor: Extract layout components to layout.py`.

### Phase 2: Helper Function Extraction

1.  **Create `dashboard_app/utils.py`**.
2.  **Move Helper Functions**: Move all general-purpose helper functions from `app.py` to `utils.py`. This includes:
    *   `parse_text_with_links`
    *   `get_cache_key`, `get_cached_processed_data`, `cache_processed_data`
    *   `get_all_keywords`
    *   `_generate_pca_insights`
    *   `get_cache_stats`
    *   `create_combined_dataset`, `create_combined_dataset2`
    *   `get_current_date_for_citation`
    *   `run_async_in_sync_context`
    *   All `create_*_figure` functions (e.g., `create_temporal_2d_figure`).
3.  **Update `app.py`**: Import the necessary helper functions from `utils.py`.
4.  **Review and Commit**:
    *   Run the application and test all features to ensure they work as expected.
    *   Commit changes with the message: `refactor: Extract helper functions to utils.py`.

### Phase 3: Callback Extraction (Iterative)

This phase is broken down into smaller sub-phases to handle the large number of callbacks.

#### Phase 3a: UI Callbacks

1.  **Create `dashboard_app/callbacks/ui_callbacks.py`**.
2.  **Move UI Callbacks**: Move all callbacks related to UI interactions to the new file. This includes callbacks for:
    *   Language switching (`update_language_store`, `update_keyword_dropdown_options`, etc.)
    *   Modal dialogs (`toggle_notes_modal`, `toggle_citation_modal`)
    *   Credits and navigation (`toggle_credits_manually`, `update_navigation_visibility`)
    *   Button states and visibility (`update_key_findings_button_text_and_state`, `update_key_findings_button_visibility`).
3.  **Create Registration Function**: In `ui_callbacks.py`, create a function `register_ui_callbacks(app)` that takes the Dash `app` object as an argument and registers all the callbacks.
4.  **Update `app.py`**: Import and call `register_ui_callbacks(app)` after the `app` object is created.
5.  **Review and Commit**:
    *   Thoroughly test all UI interactions.
    *   Commit changes with the message: `refactor: Extract UI callbacks to callbacks/ui_callbacks.py`.

#### Phase 3b: Graph & Analysis Callbacks

1.  **Create `dashboard_app/callbacks/graph_callbacks.py`**.
2.  **Move Graph Callbacks**: Move all callbacks that generate graphs and perform statistical analysis. This includes:
    *   `update_temporal_2d_analysis`, `update_temporal_slider_properties`
    *   `update_3d_plot`
    *   `update_seasonal_analysis`
    *   `update_fourier_analysis`
    *   `update_regression_analysis`
3.  **Create Registration Function**: In `graph_callbacks.py`, create a function `register_graph_callbacks(app)`.
4.  **Update `app.py`**: Import and call `register_graph_callbacks(app)`.
5.  **Review and Commit**:
    *   Test all graphing and analysis features.
    *   Commit changes with the message: `refactor: Extract graph callbacks to callbacks/graph_callbacks.py`.

#### Phase 3c: Key Findings Callbacks

1.  **Create `dashboard_app/callbacks/kf_callbacks.py`**.
2.  **Move Key Findings Callbacks**: Move the `toggle_key_findings_modal` and `save_key_findings` callbacks to this new file.
3.  **Create Registration Function**: In `kf_callbacks.py`, create a function `register_kf_callbacks(app)`.
4.  **Update `app.py`**: Import and call `register_kf_callbacks(app)`.
5.  **Review and Commit**:
    *   Test the "Key Findings" feature thoroughly.
    *   Commit changes with the message: `refactor: Extract Key Findings callbacks to callbacks/kf_callbacks.py`.

#### Phase 3d: Main Content Callback

1.  **Create `dashboard_app/callbacks/main_callbacks.py`**.
2.  **Move Main Callback**: Move the `update_main_content` callback to this new file.
3.  **Create Registration Function**: In `main_callbacks.py`, create a function `register_main_callbacks(app)`.
4.  **Update `app.py`**: Import and call `register_main_callbacks(app)`.
5.  **Review and Commit**:
    *   Perform a final end-to-end test of the application's main functionality.
    *   Commit changes with the message: `refactor: Extract main content callback to callbacks/main_callbacks.py`.

### Phase 4: Documentation Update

1.  **Update `GEMINI.md`**:
    *   Update the "app.py Detailed Analysis" section to reflect the new modular structure.
    *   Update the file structure diagram.
    *   Ensure all descriptions are still accurate.
2.  **Update `README.md`**:
    *   Review the "Project Structure" section and update it to reflect the changes.
3.  **Update `AGENTS.md` and `CLAUDE.md`**:
    *   Update the "File Organization" and any other relevant sections to reflect the new structure.
4.  **Review and Commit**:
    *   Commit the documentation updates with the message: `docs: Update documentation for app.py refactor`.

### Phase 5: Final Review and Cleanup

1.  **Review `app.py`**: Ensure that the `app.py` file is now a lean entry point, primarily responsible for:
    *   Initializing the Dash app.
    *   Importing and assigning the layout.
    *   Calling the callback registration functions.
    *   Running the application.
2.  **Cleanup**: Remove any unused imports or variables from all modified files.
3.  **Final Verification**: Perform a full regression test of the application.
4.  **Final Commit**: Commit any final cleanup changes with the message: `refactor: Final cleanup of app.py refactor`.

## 5. Git Policy

*   **Branching**: All refactoring work will be done on a dedicated feature branch (e.g., `refactor/app-py-modularization`).
*   **Commits**: A commit will be made after each sub-phase is completed and verified. Commit messages will be clear and descriptive, following the conventional commit format (e.g., `refactor: ...`, `docs: ...`).
*   **Pull Request**: Once all phases are complete, a pull request will be opened to merge the feature branch into the main branch. The pull request description will link to this refactoring plan.

By following this phased approach, we can safely and effectively refactor the `app.py` file, making the project more maintainable and scalable for the future.
