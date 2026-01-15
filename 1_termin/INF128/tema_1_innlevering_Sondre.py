print(""" *****     *****   *     *   *****    *****    *****
*     *   *     *  **    *   *    *   *    *   *
*         *     *  * *   *   *     *  *    *   *
 ****     *     *  *  *  *   *     *  *****    ****
     *    *     *  *   * *   *     *  *   *    *
*     *   *     *  *    **   *    *   *    *   *
 *****     *****   *     *   *****    *     *  *****""")

fornavn = "Sondre"
etternavn = "Fosså"

print(fornavn,etternavn)
print(etternavn, ",",fornavn)

#nok = input("Hvor mange kroner: ")
nok = "20"
dollarkurs = 10.0
dollar = int(nok) / dollarkurs
eurokurs = 11.72
euro = int(nok) / eurokurs

print(nok,"kr er ",f"{dollar:.2f}",u"\N{dollar sign}", "og " f"{euro:.2f}",u"\N{euro sign}")