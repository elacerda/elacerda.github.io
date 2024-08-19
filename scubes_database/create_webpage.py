from os.path import join
from copy import deepcopy as copy
from astropy.io import fits, ascii

CUBESPATH = '/PATH/TO/CUBES'
MASTERLIST = '/PATH/TO/MASTERLIST'

def create_index(ml):
    index_ini = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.10.2/dist/katex.min.css" integrity="sha384-yFRtMMDnQtDRO8rLpMIKrtPCD5jdktao2TV19YiZYWMDkUR5GQZR/NOVTdquEx1j" crossorigin="anonymous">
        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.10.2/dist/katex.min.js" integrity="sha384-9Nhn55MVVN0/4OFx7EE5kpFBPsEMZxKTCnA+4fqDmg12eCTqGi6+BB2LjY8brQxJ" crossorigin="anonymous"></script>
        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.10.2/dist/contrib/auto-render.min.js" integrity="sha384-kWPLUVMOks5AQFrykwIup5lo0m3iMkkHrD0uJ4H5cjeGihAutqP0yW0J6dpFiVkI" crossorigin="anonymous" onload="renderMathInElement(document.body);"></script>
        <link rel="stylesheet" href="style.css">
        <title>S-Cubes masterlist Gallery</title>
    </head>
    <body>
        <header>
            <div>
                <h1>S-Cubes</h1>
            </div>
            <div class="menu">
                <nav>
                    <ul>
                        <li><a href="https://elacerda.github.io/s-cubes/" target="_blank">Documentation</a></li>
                        <li><a href="https://github.com/elacerda/s-cubes" target="_blank">Source</a></li>
                    </ul>
                </nav>
            </div>
        </header>
        <main>
            <div class="banner"></div>
            <div class="table_wrapper">
                <table>
                    <thead>
                        <th>Image</th>
                        <th>SNAME</th>
                        <th>Name</th>
                        <th>Field</th>
                        <th>RA(degrees)</th>
                        <th>DEC(degrees)</th>
                        <th>Redshift</th>
                        <th>R50(pix)</th>
                        <th>Cube size(pix)</th>
                    </thead>
                    <tbody>
    """    
    index_cube_template = """
                        <tr class="line" data-href="{SNAME}.html">
                            <td>
                                <img src="http://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_rgb_thumb.png" alt="object image">
                            </td>
                            <td>{SNAME}</td>
                            <td>{NAME}</td>
                            <td>{FIELD}</td>
                            <td>{RA__deg}</td>
                            <td>{DEC__deg}</td>
                            <td>{REDSHIFT}</td>
                            <td>{SIZE__pix}</td>
                            <td>{SIZE}</td>
                        </tr>
    """
    index_fin = """
                    </tbody>
                </table>
            </div>
        </main>
        <footer>
            <div>
                <p>© Copyright 2024, Eduardo Alberto Duarte Lacerda</p>
            </div>
        </footer>
    </body>
    <script>
        let sel = document.querySelectorAll('.line')

        sel.forEach((e) => {
            e.addEventListener('click', ()=>{
                window.open(`http://elacerda.github.io/scubes_database/${e.dataset.href}`, `_blank`);
            })
        })
    </script>         
    </html>
    """
    gal_page_ini = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.10.2/dist/katex.min.css" integrity="sha384-yFRtMMDnQtDRO8rLpMIKrtPCD5jdktao2TV19YiZYWMDkUR5GQZR/NOVTdquEx1j" crossorigin="anonymous">
            <script defer src="https://cdn.jsdelivr.net/npm/katex@0.10.2/dist/katex.min.js" integrity="sha384-9Nhn55MVVN0/4OFx7EE5kpFBPsEMZxKTCnA+4fqDmg12eCTqGi6+BB2LjY8brQxJ" crossorigin="anonymous"></script>
            <script defer src="https://cdn.jsdelivr.net/npm/katex@0.10.2/dist/contrib/auto-render.min.js" integrity="sha384-kWPLUVMOks5AQFrykwIup5lo0m3iMkkHrD0uJ4H5cjeGihAutqP0yW0J6dpFiVkI" crossorigin="anonymous" onload="renderMathInElement(document.body);"></script>
            <link rel="stylesheet" href="style.css">
            <title>Object name | S-Cube</title>
        </head>
        <body>
            <header>
                <div>
                    <h1>S-Cubes</h1>
                </div>
                <div class="menu">
                    <nav>
                        <ul>
                            <li><a href="https://elacerda.github.io/s-cubes/" target="_blank">Documentation</a></li>
                            <li><a href="https://github.com/elacerda/s-cubes" target="_blank">Source</a></li>
                        </ul>
                    </nav>
                </div>
            </header>
    """
    gal_page_template = """

        <main>
            <div style="background-image:url(https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_imgs_3Dflux.png); display: flex; justify-content: center; align-items: center; max-height: 300px; background-position: center; background-repeat: no-repeat; background-size:contain; "></div>
            <div class="object_info_wrapper">
                <div class="object_info">
                    <h3>Object Info</h3>
                    <div>
                        <table>
                            <tbody>
                                <tr>
                                    <td class="object_table_title">SNAME</td>
                                    <td>{SNAME}</td>
                                </tr>
                                <tr>
                                    <td class="object_table_title">NAME</td>
                                    <td>{NAME}</td>
                                </tr>
                                <tr>
                                    <td class="object_table_title">FIELD</td>
                                    <td>{FIELD}</td>
                                </tr>
                                <tr>
                                    <td class="object_table_title">RA (degrees)</td>
                                    <td>{RA__deg}</td>
                                </tr>
                                <tr>
                                    <td class="object_table_title">DEC (degrees)</td>
                                    <td>{DEC__deg}</td>
                                </tr>
                                <tr>
                                    <td class="object_table_title">Redshift</td>
                                    <td>{REDSHIFT}</td>
                                </tr>
                                <tr>
                                    <td class="object_table_title">R50 (pix)</td>
                                    <td>{SIZE__pix}</td>
                                </tr>
                                <tr>
                                    <td class="object_table_title">Cube size (pix)</td>
                                    <td>{SIZE}</td>
                                </tr>
                                <tr>
                                    <td colspan=2><a href="http://minerva.ufsc.br/~lacerda/s-cubes/cubes/{SNAME}_cube.fits" target="_blank">Download SCUBE (FITS)</a></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <img src="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_rgb.png" alt=""  class="object_img">
            </div>
            <div>
                <details>
                    <summary>Images</summary>
                    <a href="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_imgs_flux.png" target="_blank"><img src="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_imgs_flux.png" style="max-width:1000px;width:100%" alt=""  class="object_img"></a><br>
                    Images in the 12 bands. Log flux density, in units of \\(10^{-18}\\) erg/s/cm\\(^2\\)/\\(\\text{\\r{A}}\\).<br><br>
                    <a href="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_imgs_SN.png" target="_blank"><img src="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_imgs_SN.png" style="max-width:1000px;width:100%" alt=""  class="object_img"></a><br>
                    Signal-to-noise ratio images in the 12 bands.<br><br>
                    <a href="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_imgs_mag.png" target="_blank"><img src="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_imgs_mag.png" style="max-width:1000px;width:100%" alt=""  class="object_img"></a><br>
                    Surface brightness images, in AB mag per arcsec\\(^2\\).<br><br>
                    <a href="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_imgs_emag.png" target="_blank"><img src="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_imgs_emag.png" style="max-width:1000px;width:100%" alt=""  class="object_img"></a><br>
                    Uncertainty images, in AB mag per arcsec\\(^2\\).<br><br>
                </details>
            </div>
            <div class="other_plot_wrapper">
                <div>
                    <details>
                        <summary>RGBs</summary>
                        Different types of RGBs composites. The filters used to R, G and B respectively are indicated at the top of each plot.<br><br>
                        <a href="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_RGB_8-5-01234.png" target="_blank"><img src="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_RGB_8-5-01234.png" style="max-width:600px;width:100%" alt=""></a><br>
                        <a href="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_RGB_8-7-5.png" target="_blank"><img src="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_RGB_8-7-5.png" style="max-width:600px;width:100%" alt=""></a><br>
                        <a href="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_RGB_8-9-0.png" target="_blank"><img src="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_RGB_8-9-0.png" style="max-width:600px;width:100%" alt=""></a><br>
                        <a href="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_RGB_8-9-5.png" target="_blank"><img src="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_RGB_8-9-5.png" style="max-width:600px;width:100%" alt=""></a><br>
                        <a href="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_RGB_9-7-5.png" target="_blank"><img src="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_RGB_9-7-5.png" style="max-width:600px;width:100%" alt=""></a><br>
                        <a href="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_RGB_9-345-012.png" target="_blank"><img src="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_RGB_9-345-012.png" style="max-width:600px;width:100%" alt=""></a><br>
                        <a href="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_RGB_11-5-0.png" target="_blank"><img src="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_RGB_11-5-0.png" style="max-width:600px;width:100%" alt=""></a><br>
                    </details>
                </div>
                <div>
                    <details>
                        <summary>Spectra</summary>
                        <a href="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_sky_spec_iso25med10.png"><img src="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_sky_spec_iso25med10.png" style="max-width:1000px;width:100%" alt=""></a><br>
                        <i>Left</i>: Sky mask. Pixels in black are considered sky. <i>Right</i>: Photo-spectra of all sky-spaxels (in gray). The black points and error bars show the mean sky fluxes and its standard deviation.<br><br>
                        <a href="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_LRGB_centspec.png"><img src="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_LRGB_centspec.png" style="max-width:1000px;width:100%" alt=""></a><br>
                        <i>Left</i>: Composite made with the iSDSS, rSDSS, and gSDSS bands in the R, G, and B channels, respectively.
                        <i>Right</i>: Photo-spectrum of the central spaxel. The lower panel shows the transmission curves of the S-PLUS filters. Dotted vertical lines mark the wavelengths of [OII]3727, [OIII]5007, and H\\(\\alpha\\)6563 at the redshift of the galaxy.<br><br>
                        <a href="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_rings_spec.png"><img src="https://minerva.ufsc.br/~lacerda/s-cubes/img/{SNAME}_rings_spec.png" style="max-width:1000px;width:100%" alt=""></a><br>
                        <i>Left</i>: Map of the galaxy showing the circular rings used to create the ring-averaged photo-spectra on the right. The rings are coloured by the distance to the nuclues.
                        <i>Right</i>: Mean photo-spectra in circular annulii of 10 pixels, in units of \\(10^{-18}\\) erg/s/cm\\(^2\\)/\\(\\text{\\r{A}}\\) per pixel, and coloured by the same colors used in <i>left</i> plot. The dotted horizontal lines mark the flux-density levels corresponding to r-band surface brightnesses 23, 24, and 25 AB mag/arcsec\\(^2\\).<br><br>
                    </details>
                </div>
            </div>
        </main>
    """
    gal_page_fin = """
        <footer>
            <div>
                <p>© Copyright 2024, Eduardo Alberto Duarte Lacerda</p>
            </div>
        </footer>
    </body>
    </html>
    """

    with open(f'index.html', 'w') as f:
        print(index_ini, file=f)
    
    for i_gal in range(len(ml)):
        gal_ml = ml[i_gal]
        gal_sname = gal_ml['SNAME']
        gal_page = copy(gal_page_template)
        index_cube = copy(index_cube_template)

        with open(f'{gal_sname}.html', 'w') as f:
            print(gal_page_ini, file=f)

        for col in ml.colnames:
            k = '{' + col + '}'
            if k in gal_page:
                gal_page = gal_page.replace(k, str(ml[i_gal][col]))
            if k in index_cube:
                index_cube = index_cube.replace(k, str(ml[i_gal][col]))
        
        # SIZE
        h = fits.getheader(join(CUBESPATH, f'{gal_sname}_cube.fits'), 0)
        size = h.get('SIZE')
        gal_page = gal_page.replace('{SIZE}', str(size))
        index_cube = index_cube.replace('{SIZE}', str(size))

        with open(f'index.html', 'a') as f:
            print(index_cube, file=f)

        with open(f'{gal_sname}.html', 'a') as f:
            print(gal_page, file=f)

        with open(f'{gal_sname}.html', 'a') as f:
            print(gal_page_fin, file=f)

    with open(f'index.html', 'a') as f:
        print(index_fin, file=f)

if __name__ == '__main__':
    ml_table = ascii.read(MASTERLIST)
    create_index(ml_table)






