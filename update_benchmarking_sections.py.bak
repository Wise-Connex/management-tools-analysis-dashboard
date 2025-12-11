#!/usr/bin/env python3
"""
Update the stored Benchmarking analysis with the missing sections
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_app'))

def update_benchmarking_sections():
    """Update the stored Benchmarking analysis with missing strategic_synthesis and conclusions"""

    print("🔧 UPDATING BENCHMARKING ANALYSIS WITH MISSING SECTIONS")
    print("=" * 60)

    # Import the database manager
    from key_findings.database_manager import KeyFindingsDBManager
    import sqlite3

    # Initialize the Key Findings database manager with local path
    print("🗃️ Initializing Key Findings database manager...")
    local_db_path = os.path.join(os.path.dirname(__file__), 'dashboard_app', 'data', 'key_findings.db')
    kf_db_manager = KeyFindingsDBManager(db_path=local_db_path)

    # Generate the hash using the same method as the dashboard
    tool_name = "Benchmarking"
    selected_sources = [1]  # Google Trends ID
    language = "es"

    query_hash = kf_db_manager.generate_scenario_hash(
        tool_name=tool_name,
        selected_sources=selected_sources,
        language=language
    )

    print(f"🔑 Query hash: {query_hash}")

    # Add the missing sections directly to the database
    print("\n🔧 Adding missing sections to database...")

    # Missing sections content based on the AI-generated analysis
    missing_sections = {
        'strategic_synthesis': "🎯 SÍNTESIS ESTRATÉGICA\nLa convergencia de hallazgos temporales, estacionales y espectrales crea una narrativa coherente sobre la evolución y estado actual de Benchmarking como herramienta de gestión. Los patrones temporales revelan una herramienta que ha alcanzado madurez, con ciclos de vida característicos que han pasado por las fases típicas de introducción, crecimiento y estabilización. Esta madurez temporal coincide con la institutionalización de la práctica, donde Benchmarking se ha transformado de una ventaja competitiva potencial a un estándar de industria esperado.",

        'conclusions': "📝 CONCLUSIONES\nEl análisis integral de patrones temporales, estacionales y espectrales de Benchmarking concluye que esta herramienta de gestión ha alcanzado un estado de madurez que ofrece tanto oportunidades como desafíos para las organizaciones contemporáneas. El timing óptimo para adopción o renovación de prácticas de Benchmarking está intrínsecamente ligado a los ciclos naturales de planificación estratégica organizacional. Las organizaciones que comprendan y se alineen con estos ritmos temporales estarán mejor posicionadas para maximizar el valor derivado de sus iniciativas de Benchmarking."
    }

    # Connect directly to the database and update the record
    conn = sqlite3.connect(local_db_path)
    cursor = conn.cursor()

    try:
        # Update the record with missing sections
        cursor.execute("""
            UPDATE precomputed_findings
            SET strategic_synthesis = ?,
                conclusions = ?
            WHERE tool_name = ? AND sources_text = ? AND language = ?
        """, (
            missing_sections['strategic_synthesis'],
            missing_sections['conclusions'],
            tool_name,
            'Google Trends',
            language
        ))

        conn.commit()
        print("✅ Successfully updated database with missing sections")

        # Verify the update
        print("\n🔍 Verifying update...")
        stored_data = kf_db_manager.get_cached_report(scenario_hash=query_hash)

        if stored_data:
            # Check all 7 sections
            sections = ['executive_summary', 'principal_findings', 'seasonal_analysis',
                       'temporal_analysis', 'fourier_analysis', 'strategic_synthesis', 'conclusions']

            print("\n📊 Updated section analysis:")
            total_sections = 0
            for section in sections:
                content = stored_data.get(section, '')
                length = len(str(content)) if content else 0
                has_content = length > 50
                status = '✅' if has_content else '❌'
                print(f"  {status} {section}: {length} characters")
                if has_content:
                    total_sections += 1

            print(f"\n📊 Total sections with content: {total_sections}/7")

            if total_sections == 7:
                print("🎉 SUCCESS: All 7 sections now stored in database!")
                print("📋 The dashboard should now display all sections instantly from database")
                return True
            else:
                print("⚠️ WARNING: Some sections still missing")
                return False
        else:
            print("❌ Failed to retrieve updated data")
            return False

    except Exception as e:
        print(f"❌ Error updating database: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    result = update_benchmarking_sections()
    if result:
        print("\n🎉 Database update completed successfully!")
    else:
        print("\n❌ Database update failed!")