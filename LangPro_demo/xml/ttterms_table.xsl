<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="html" encoding="utf-8" doctype-system="about:legacy-compat"/>
    <xsl:template match="/">
        <html>
            <head>
                <!-- 
                <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js">//</script>
                <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.9.2/jquery-ui.min.js">//</script>
                <script type="text/javascript" src="PATH_TO/jquery.jsPlumb-1.5.4-min.js ">//</script>
                -->
                <script type="text/javascript" src="jquery-1.12.4.min.js"></script>
                <script type="text/javascript" src="myfunctions.js "></script>
                <link rel="stylesheet" type="text/css" href="ttterms.css"/>
                <title>TTterms</title>
            </head>
            <body style="text-align:center;">
                <xsl:apply-templates/>
            </body>
        </html>
    </xsl:template>

    <!-- ####################### LIST OF TEMPLATES ####################### -->

    <xsl:template match="fullttterm">
        <div class="fullttterm">
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="ttterm">
        <table class="ttterm">
            <tr>
                <td class="ttexp">
                    <xsl:apply-templates select="var|tlp|app|abst"/>
                </td>
            </tr>
            <tr>
                <td class="type">
                    <xsl:apply-templates select="type"/>
                </td>
            </tr>
        </table>
    </xsl:template>


    <xsl:template match="tlp">
        <table class="tlp">
            <tr>
                <td class="lem">
                    <xsl:value-of select="lem"/>
                </td>
            </tr>
            <tr>
                <td class="tok">
                    <xsl:value-of select="tok"/>
                </td>
            </tr>
            <tr>
                <td class="pos">
                    <xsl:value-of select="pos"/>
                </td>
            </tr>
            <tr>
                <td class="ner">
                    <xsl:value-of select="ner"/>
                </td>
            </tr>
        </table>
    </xsl:template>

    <xsl:template match="var">
        <span>
            <xsl:value-of select="."/>
        </span>
    </xsl:template>

    <xsl:template match="app">
        <span class="app">
            <xsl:apply-templates select="ttterm"/>
        </span>
    </xsl:template>

    <xsl:template match="abst">
        <div class="ttterm">
            <div class="lambda">
                <xsl:text>&#955;</xsl:text>
            </div>
            <table class="lamx">
                <tr>
                    <td>
                        <xsl:value-of select="ttterm[1]/var"/>
                    </td>
                </tr>
                <tr>
                    <td class="type">
                        <xsl:value-of select="ttterm[1]/type"/>
                    </td>
                </tr>
            </table>
        </div>
        <xsl:apply-templates select="ttterm[2]"/>
    </xsl:template>


    <xsl:template match="type">
        <xsl:copy-of select="."/>
    </xsl:template>




</xsl:stylesheet>
