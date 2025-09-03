"""
Core Application Operations
"""
import os
import sys
import threading
from datetime import datetime
from tkinter import messagebox, filedialog

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.ui_components import show_notification
from src.utils.item_details import show_item_details


class AppOperations:
    """Mixin class for application operations"""

    def filter_collections(self, event=None):
        """Filter collections based on search input"""
        search_term = self.collection_search.get().lower()

        # Skip filtering if it's the placeholder text
        if search_term == "type to search countries...":
            return

        # Clear existing items
        for item in self.collections_tree.get_children():
            self.collections_tree.delete(item)

        # Filter and display matching collections
        filtered_collections = []
        for collection in self.collections:
            collection_name = collection.get('title', collection.get('id', '')).lower()
            collection_id = collection.get('id', '').lower()

            # Search in both title and ID
            if (not search_term or
                    search_term in collection_name or
                    search_term in collection_id):
                filtered_collections.append(collection)

        # Sort filtered collections alphabetically by title
        sorted_filtered_collections = sorted(filtered_collections,
                                             key=lambda x: x.get('title', x.get('id', '')).lower())

        # Display filtered collections
        for collection in sorted_filtered_collections:
            title = collection.get('title', collection.get('id', 'Unknown'))
            collection_id = collection.get('id', 'Unknown')

            # Get last updated date
            last_updated = (collection.get('last_modified') or "Unknown")

            # Format date if it's a full ISO string
            if isinstance(last_updated, str) and 'T' in last_updated:
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                    last_updated = dt.strftime('%Y-%m-%d')
                except:
                    last_updated = last_updated[:10]

            # Insert with collection data stored in tags
            item_id = self.collections_tree.insert('', 'end', text='☐',
                                                   values=(title, last_updated, '🔍 Thumbnail', '📋 Metadata'))
            # Store collection info as a way to retrieve it later
            self.collections_tree.item(item_id, tags=(collection_id,))

        # Update collection count
        self.update_stats()

    def toggle_collection_selection(self, event):
        """Toggle selection of collections in tree"""
        # Get the item that was clicked
        item = self.collections_tree.identify('item', event.x, event.y)
        if not item:
            return

        # Toggle selection
        current_text = self.collections_tree.item(item, 'text')
        if current_text == '☐':
            self.collections_tree.item(item, text='☑')
        else:
            self.collections_tree.item(item, text='☐')

        # Update statistics immediately
        self.update_stats()

    def select_all_collections(self):
        """Select all available collections"""
        for item in self.collections_tree.get_children():
            self.collections_tree.item(item, text='☑')
        self.update_stats()

    def select_recent_years(self):
        """Select recent years (2020-2030)"""
        for year, var in self.year_vars.items():
            var.set(year >= 2020)

    def select_high_resolution(self):
        """Select only 100m resolution"""
        self.resolution_vars['100m'].set(True)
        self.resolution_vars['1km'].set(False)

    def select_all_years(self):
        """Select all years"""
        for var in self.year_vars.values():
            var.set(True)

    def clear_all_years(self):
        """Clear all year selections"""
        for var in self.year_vars.values():
            var.set(False)

    def export_results(self):
        """Export search results to CSV"""
        # Implementation for exporting results
        pass

    def clear_all(self):
        """Clear all selections and results"""
        self.clear_selection()
        self.search_results = []
        self.update_search_results()

    def show_selected_item_details(self):
        """Show details of selected item"""
        # Get currently selected item from results tree
        selection = self.results_tree.selection()
        if not selection:
            show_notification(self.root, "Please select an item to view details", "warning")
            return

        # Get the first selected item
        tree_item = selection[0]
        item_index = self.results_tree.index(tree_item)

        if item_index < len(self.search_results):
            selected_item = self.search_results[item_index]

            # Get item info
            item_id = selected_item.get('id', '').lower()
            if 'agesex' in item_id:
                info = self.get_agesex_info(selected_item)
            else:
                info = self.get_population_info(selected_item)

            # Show details dialog
            show_item_details(self.root, selected_item, info)

    def go_to_downloads(self):
        """Navigate to downloads tab"""
        self.notebook.select(2)  # Switch to downloads tab

    def show_item_context_menu(self, event):
        """Show context menu for items"""
        # Implementation for context menu
        pass

    def load_collections(self):
        """Load collections from API"""

        def fetch_collections():
            try:
                self.collections = self.client.get_collections()
                self.root.after(0, self.update_collections_display)
                self.root.after(0, lambda: self.connection_status.config(
                    text="Connected", style='Success.TLabel'))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load collections: {e}"))
                self.root.after(0, lambda: self.connection_status.config(
                    text="Connection Error", style='Error.TLabel'))

        threading.Thread(target=fetch_collections, daemon=True).start()

    def update_collections_display(self):
        """Update the collections tree display"""
        # Clear existing items
        for item in self.collections_tree.get_children():
            self.collections_tree.delete(item)

        # Sort collections alphabetically by title
        sorted_collections = sorted(self.collections, key=lambda x: x.get('title', x.get('id', '')).lower())

        # Add collections to tree with available data
        for collection in sorted_collections:
            title = collection.get('title', collection.get('id', 'Unknown'))
            collection_id = collection.get('id', 'Unknown')

            # Get last updated date (same logic as filter_collections)
            last_updated = (collection.get('last_modified') or
                            "Unknown")

            # Format date if it's a full ISO string
            if isinstance(last_updated, str) and 'T' in last_updated:
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                    last_updated = dt.strftime('%Y-%m-%d')
                except:
                    last_updated = last_updated[:10]  # Just take the date part

            # Insert with collection data stored in tags
            item_id = self.collections_tree.insert('', 'end', text='☐',
                                                   values=(title, last_updated, '🔍 Thumbnail', '📋 Metadata'))
            # Store collection ID in tags for retrieval
            self.collections_tree.item(item_id, tags=(collection_id,))

        self.update_stats()

    def search_items(self):
        """Enhanced search with progress indication"""
        # Get selected collections from tree using tags (not indices due to sorting)
        selected_collections = []
        for item in self.collections_tree.get_children():
            if self.collections_tree.item(item, 'text') == '☑':
                # Get collection ID from tags instead of using index
                tags = self.collections_tree.item(item, 'tags')
                if tags and len(tags) > 0:
                    collection_id = tags[0]  # First tag is the collection ID
                    selected_collections.append(collection_id)

        if not selected_collections:
            show_notification(self.root, "Please select at least one collection", "warning")
            return

        # Get selected filter values
        selected_years = [year for year, var in self.year_vars.items() if var.get()]
        selected_resolutions = [res for res, var in self.resolution_vars.items() if var.get()]
        selected_projects = [proj for proj, var in self.project_vars.items() if var.get()]

        self.search_status.config(text="Searching...")
        self.search_button.config(state="disabled")
        self.search_progress.start()

        def perform_search():
            try:
                # Build CQL2 JSON filter for multiple values using OR
                def build_or_condition(field, values):
                    """Build OR condition for multiple values"""
                    if len(values) == 1:
                        return {"op": "=", "args": [{"property": field}, values[0]]}
                    else:
                        conditions = [{"op": "=", "args": [{"property": field}, value]} for value in values]
                        return {"op": "or", "args": conditions}

                cql_conditions = []

                # Add conditions for each filter
                if selected_years:
                    cql_conditions.append(build_or_condition("year", selected_years))

                if selected_resolutions:
                    cql_conditions.append(build_or_condition("resolution", selected_resolutions))

                if selected_projects:
                    cql_conditions.append(build_or_condition("project", selected_projects))

                # Combine all conditions with AND
                filter_json = None
                if cql_conditions:
                    if len(cql_conditions) == 1:
                        filter_json = cql_conditions[0]
                    else:
                        filter_json = {"op": "and", "args": cql_conditions}

                # Update progress
                self.root.after(0, lambda: self.search_status.config(text="Sending search request..."))

                # Single optimized search request using CQL2 JSON
                results = self.client.search_items(
                    collections=selected_collections,
                    filter_expr=filter_json,
                    filter_lang="cql2-json" if filter_json else None,
                    limit=10000  # Increased limit since we're doing one request
                )

                self.search_results = results
                self.root.after(0, self.update_search_results)
                self.root.after(0, lambda: show_notification(
                    self.root, f"Found {len(results)} items", "success"))

            except Exception as e:
                self.root.after(0, lambda: show_notification(
                    self.root, f"Search failed: {e}", "error"))
            finally:
                self.root.after(0, lambda: self.search_button.config(state="normal"))
                self.root.after(0, lambda: self.search_progress.stop())
                self.root.after(0, lambda: self.search_status.config(text="Search completed"))

        threading.Thread(target=perform_search, daemon=True).start()

    def update_search_results(self):
        """Update search results display"""
        # Clear existing results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Update summary
        count = len(self.search_results)
        self.results_summary.config(text=f"Found {count} items")

        # Populate tree with enhanced information
        for item in self.search_results:
            properties = item.get('properties', {})
            item_id = item.get('id', '').lower()

            # Get file size and date using specialized functions
            if 'agesex' in item_id:
                info = self.get_agesex_info(item)
            else:
                info = self.get_population_info(item)

            file_size = info['size']
            last_updated = info['last_updated']

            # Format date nicely if available
            if last_updated != 'Unknown':
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                    last_updated = dt.strftime('%Y-%m-%d')
                except:
                    pass

            # Determine file type based on download type
            file_type = "ZIP" if info['download_type'] == 'Archive' else "TIF"

            values = (
                item.get('collection', 'Unknown'),
                item.get('id', 'Unknown'),
                properties.get('year', 'Unknown'),
                properties.get('resolution', 'Unknown'),
                properties.get('project', 'Unknown').replace('Global2_', ''),
                file_type,
                file_size,
                last_updated,
                '📋 Details'  # Add Details button column
            )

            self.results_tree.insert('', 'end', text='☐', values=values, tags=('unselected',))

        # Update statistics
        self.update_stats()

        # Show/hide placeholder based on results count
        if count > 0:
            self.results_tree.tkraise()  # Show tree
            self.notebook.select(1)  # Switch to results tab
        else:
            self.results_placeholder.tkraise()  # Show placeholder

    def toggle_item_selection(self, event):
        """Toggle item selection in results"""
        # Get the item that was clicked
        item = self.results_tree.identify('item', event.x, event.y)
        if not item:
            return

        # Get item index to find in search_results
        item_index = self.results_tree.index(item)
        if item_index >= len(self.search_results):
            return

        # Toggle selection
        current_text = self.results_tree.item(item, 'text')
        result_item = self.search_results[item_index]

        if current_text == '☐':
            # Select item
            self.results_tree.item(item, text='☑', tags=('selected',))
            if result_item not in self.selected_items:
                self.selected_items.append(result_item)
        else:
            # Deselect item
            self.results_tree.item(item, text='☐', tags=('unselected',))
            if result_item in self.selected_items:
                self.selected_items.remove(result_item)

        # Update selected tree and statistics
        self.update_selected_tree()
        self.update_stats()

    def select_all_results(self):
        """Select all search results"""
        self.selected_items = self.search_results.copy()
        for item in self.results_tree.get_children():
            self.results_tree.item(item, text='☑', tags=('selected',))
        self.update_selected_tree()
        self.update_stats()

    def clear_selection(self):
        """Clear all selected items"""
        self.selected_items.clear()
        for item in self.results_tree.get_children():
            self.results_tree.item(item, text='☐')
        self.update_selected_tree()
        self.update_stats()

    def select_download_dir(self):
        """Select download directory"""
        directory = filedialog.askdirectory(initialdir=self.download_dir.get())
        if directory:
            self.download_dir.set(directory)

    def start_download(self):
        """Start downloading selected items with enhanced progress tracking"""
        if not self.selected_items:
            show_notification(self.root, "No items selected for download", "warning")
            return

        if not os.path.exists(self.download_dir.get()):
            try:
                os.makedirs(self.download_dir.get(), exist_ok=True)
            except Exception as e:
                show_notification(self.root, f"Cannot create download directory: {e}", "error")
                return

        # Update UI state for active download
        self.download_active.set(True)
        self.download_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.progress_var.set(0)

        # Initialize download stats
        self.download_start_time = datetime.now()
        self.bytes_downloaded = 0
        self.total_bytes = 0

        def download_files():
            total_files = len(self.selected_items)
            downloaded_files = 0
            failed_files = 0

            for i, item in enumerate(self.selected_items):
                # Check if download was stopped
                if not self.download_active.get():
                    break

                # Get download URL from appropriate asset
                assets = item.get('assets', {})
                download_url = None
                filename = f"{item.get('id', 'unknown')}.tif"
                item_id = item.get('id', '').lower()

                # For age-sex data, prefer archive over individual files
                if 'agesex' in item_id:
                    # Look for archive asset first
                    for asset_name, asset in assets.items():
                        if 'archive' in asset.get('roles', []) or 'arch' in asset_name.lower():
                            download_url = asset.get('href')
                            if download_url:
                                # Extract filename from URL if possible
                                if '/' in download_url:
                                    filename = download_url.split('/')[-1]
                                else:
                                    filename = f"{item.get('id', 'unknown')}_archive.zip"
                            break

                    # If no archive found, fall back to first data asset
                    if not download_url:
                        for asset_name, asset in assets.items():
                            if 'data' in asset.get('roles', []):
                                download_url = asset.get('href')
                                if download_url:
                                    if '/' in download_url:
                                        filename = download_url.split('/')[-1]
                                break
                else:
                    # For population data, use standard data asset
                    for asset_name, asset in assets.items():
                        if 'data' in asset.get('roles', []):
                            download_url = asset.get('href')
                            if download_url:
                                # Extract filename from URL if possible
                                if '/' in download_url:
                                    filename = download_url.split('/')[-1]
                            break

                if not download_url:
                    failed_files += 1
                    continue

                # Create folder structure if requested
                if self.create_subfolders.get():
                    # Extract country and year from item data
                    country = item.get('collection', 'Unknown')
                    properties = item.get('properties', {})
                    year = str(properties.get('year', 'Unknown'))

                    # Create country/year folder structure
                    subfolder = os.path.join(self.download_dir.get(), country, year)
                    os.makedirs(subfolder, exist_ok=True)
                    local_path = os.path.join(subfolder, filename)
                else:
                    local_path = os.path.join(self.download_dir.get(), filename)

                # Update progress with current file
                progress = (i / total_files) * 100
                current_time = datetime.now()
                elapsed = (current_time - self.download_start_time).total_seconds()

                def update_ui():
                    self.progress_var.set(progress)
                    self.progress_label.config(text=f"Downloading {filename}")

                    stats_text = f"Files: {downloaded_files}/{total_files}"
                    if failed_files > 0:
                        stats_text += f" (Failed: {failed_files})"
                    self.download_stats.config(text=stats_text)

                    # Clear speed display
                    self.speed_label.config(text="")

                self.root.after(0, update_ui)

                # Update selected tree status for current file
                def update_tree_status(status):
                    for tree_item in self.selected_tree.get_children():
                        values = self.selected_tree.item(tree_item, 'values')
                        if filename in values[0]:  # Match by filename in item name
                            self.selected_tree.item(tree_item, values=(values[0], values[1], status))
                            break

                self.root.after(0, lambda: update_tree_status("Downloading..."))

                # Download file
                success = self.client.download_file(download_url, local_path)

                if success:
                    downloaded_files += 1
                    self.root.after(0, lambda: update_tree_status("✅ Complete"))
                else:
                    failed_files += 1
                    self.root.after(0, lambda: update_tree_status("❌ Failed"))

            # Download completed or stopped
            def finalize_download():
                self.download_active.set(False)
                self.download_button.config(state="normal")
                self.stop_button.config(state="disabled")
                self.progress_var.set(
                    100 if downloaded_files == total_files else (downloaded_files / total_files) * 100)

                if downloaded_files == total_files:
                    self.progress_label.config(text="All downloads completed!")
                    show_notification(self.root, f"Successfully downloaded {downloaded_files} files", "success")
                elif downloaded_files > 0:
                    self.progress_label.config(text=f"Downloaded {downloaded_files}/{total_files} files")
                    show_notification(self.root, f"Downloaded {downloaded_files}/{total_files} files", "info")
                else:
                    self.progress_label.config(text="Download failed")
                    show_notification(self.root, "Download failed", "error")

                # Final stats
                elapsed = (datetime.now() - self.download_start_time).total_seconds()
                stats_text = f"Completed: {downloaded_files}/{total_files}"
                if failed_files > 0:
                    stats_text += f" | Failed: {failed_files}"
                stats_text += f" | Time: {int(elapsed // 60)}m {int(elapsed % 60)}s"
                self.download_stats.config(text=stats_text)
                self.speed_label.config(text="")

            self.root.after(0, finalize_download)

        threading.Thread(target=download_files, daemon=True).start()

    def update_download_progress(self, progress: float, status: str):
        """Update download progress"""
        self.progress_var.set(progress)
        self.progress_label.config(text=status)

    def get_population_info(self, item):
        """Get information for population data items"""
        properties = item.get('properties', {})
        size = properties.get('size')
        last_updated = properties.get('datetime')

        return {
            'size': size,
            'download_type': 'Data File',
            'last_updated': last_updated
        }

    def get_agesex_info(self, item):
        """Get information for age-sex data items"""
        properties = item.get('properties', {})
        assets = item.get('assets', {})

        # For age-sex data, prefer archive
        size = "Unknown"
        for asset_name, asset in assets.items():
            if 'arch' in asset_name.lower():
                size = asset.get('file:size', 'Unknown')
                break

        # Get last updated date
        last_updated = properties.get('datetime')
        return {
            'size': size,
            'download_type': 'Archive',
            'last_updated': last_updated
        }

    def update_selected_tree(self):
        """Update selected items tree in download tab"""
        # Clear existing items

        for item in self.selected_tree.get_children():
            self.selected_tree.delete(item)

        # Show/hide placeholder based on selected items
        if not self.selected_items:
            self.selected_placeholder.tkraise()
        else:
            self.selected_tree.tkraise()

            # Add selected items
            for item in self.selected_items:
                properties = item.get('properties', {})
                item_id = item.get('id', '').lower()

                # Get information based on data type
                if 'agesex' in item_id:
                    info = self.get_agesex_info(item)
                else:
                    info = self.get_population_info(item)

                item_name = item.get('id')
                item_title = properties.get('title')
                collection = item.get('collection')
                file_type = "ZIP" if info['download_type'] == 'Archive' else "TIF"

                self.selected_tree.insert('', 'end',
                                          values=(item_title, collection, item_name, file_type, info['size'], "Ready"))
