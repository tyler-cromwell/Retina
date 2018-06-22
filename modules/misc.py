#######################################################################
# Copyright (C) 2016-Present Tyler Cromwell <tjc6185@gmail.com>
#
# This file is part of Retina.
#
# Retina is free software: you can redistribute it and/or modify
# it under Version 2 of the terms of the GNU General Public License
# as published by the Free Software Foundation.
#
# Retina is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY of FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Retina.
# If not, see <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>
#######################################################################

try:
    import tkinter

    def get_display_resolution():
        tk = tkinter.Tk()
        width = tk.winfo_screenwidth()
        height = tk.winfo_screenheight()
        return (width, height)

except ImportError as ie:
    def get_display_resolution():
        return (0, 0)
