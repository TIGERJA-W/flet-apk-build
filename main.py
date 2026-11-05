import flet as ft
import os
import time
# Remove the flet_fastapi import line completely



def main(page: ft.Page):
    page.title = "Storage Cleaner Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 380
    page.window_height = 700

    # Layout state variables
    status_text = ft.Text("Ready to Clean", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_200)
    progress_bar = ft.ProgressBar(width=300, value=0.0, color=ft.colors.GREEN, bgcolor=ft.colors.BLACK26)
    stats_display = ft.Text("Junk Space Found: 0.00 MB", size=14, color=ft.colors.WHITE70)
    
    # Mocking a phone storage directory inside your project folder for demonstration
    mock_storage_path = "./mock_phone_storage"

    def ensure_mock_files_exist():
        """Creates dummy junk files for testing the cleaner app logic."""
        if not os.path.exists(mock_storage_path):
            os.makedirs(mock_storage_path)
        # Create a few fake logs and temp files if they aren't there
        for i in range(1, 6):
            with open(os.path.join(mock_storage_path, f"temp_log_{i}.log"), "w") as f:
                f.write("A" * (i * 1024 * 250)) # Creates files around 250KB - 1.2MB
            with open(os.path.join(mock_storage_path, f"cache_data_{i}.tmp"), "w") as f:
                f.write("B" * (i * 1024 * 150))

    def start_scanning(e):
        scan_button.disabled = True
        status_text.value = "Scanning phone storage..."
        progress_bar.value = None # Turns on loading animation
        page.update()
        
        ensure_mock_files_exist()
        time.sleep(2) # Simulating scan delay
        
        junk_extensions = ['.tmp', '.log', '.cache']
        total_bytes = 0
        found_files = []

        for root, _, files in os.walk(mock_storage_path):
            for file in files:
                if any(file.endswith(ext) for ext in junk_extensions):
                    path = os.path.join(root, file)
                    total_bytes += os.path.getsize(path)
                    found_files.append(path)

        mb_saved = total_bytes / (1024 * 1024)
        
        # Update UI with scan results
        progress_bar.value = 1.0
        status_text.value = f"Scan Complete! Found {len(found_files)} junk files."
        status_text.color = ft.colors.GREEN_400
        stats_display.value = f"Junk Space Found: {mb_saved:.2f} MB"
        
        if total_bytes > 0:
            clean_button.visible = True
            # Store files to delete in clean button's data attribute
            clean_button.data = found_files 
        
        scan_button.disabled = False
        page.update()

    def start_cleaning(e):
        status_text.value = "Deleting temporary files..."
        progress_bar.value = None
        clean_button.visible = False
        page.update()
        
        time.sleep(1.5) # Simulating deletion work
        
        files_to_remove = clean_button.data
        if files_to_remove:
            for file_path in files_to_remove:
                try:
                    os.remove(file_path)
                except Exception:
                    pass

        status_text.value = "Storage Optimized Successfully!"
        status_text.color = ft.colors.BLUE_200
        stats_display.value = "Junk Space Cleared: 0.00 MB"
        progress_bar.value = 0.0
        page.update()

    # Buttons
    scan_button = ft.ElevatedButton(
        text="Scan Storage", 
        icon=ft.icons.SEARCH, 
        on_click=start_scanning,
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_600)
    )
    
    clean_button = ft.ElevatedButton(
        text="Clean Junk Now", 
        icon=ft.icons.DELETE_FOREVER, 
        on_click=start_cleaning,
        visible=False,
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.RED_ACCENT_400)

    )

    # App Layout View (Phone Card View)
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(name=ft.icons.PHONELINK_SETUP, size=50, color=ft.colors.BLUE_400),
                    ft.Text("CleanerEngine v1.0", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=20, color=ft.colors.WHITE24),
                    status_text,
                    ft.Container(height=10),
                    progress_bar,
                    ft.Container(height=10),
                    stats_display,
                    ft.Container(height=30),
                    scan_button,
                    ft.Container(height=10),
                    clean_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=30,
            border_radius=20,
            bgcolor=ft.colors.SURFACE_VARIANT,
            width=340,
            height=600,
            alignment=ft.alignment.center,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)  # This is the exact syntax version 0.19.0 needs!


