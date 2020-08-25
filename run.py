import os

from census_rm_ops_ui.setup import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=os.getenv('PORT', '8234'))
