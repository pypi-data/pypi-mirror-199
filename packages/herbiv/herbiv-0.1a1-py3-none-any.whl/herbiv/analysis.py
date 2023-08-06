from . import chemical_protein
from . import chemical
from . import tcm_chemical
from . import tcm
from . import output


def reverse(genes,
            protein_chemical_links_path='data/HerbiV_chemical_protein_links.csv',
            score=900,
            save=True,
            chemicals_path='data/HerbiV_chemicals.csv',
            tcm_chemical_links_path='data/HerbiV_tcm_chemical_links.csv',
            tcm_path='data/HerbiV_tcm.csv'):
    r"""
    进行逆向网络药理学分析
    :param genes: 字典类型，存储拟分析蛋白（基因）在STITCH中的ID与其名称的对应关系
    :param protein_chemical_links_path: 字符串类型，HerbiV_chemical_protein_links数据集的路径
    :param score: int类型，仅combined_score大于等于score的记录会被筛选出
    :param save: 布尔类型，是否保存原始分析结果
    :param chemicals_path: 字符串类型，HerbiV_chemicals数据集的路径
    :param tcm_chemical_links_path: 字符串类型，HerbiV_tcm_chemical_links数据集的路径
    :param tcm_path: 字符串类型，HerbiV_tcm数据集的路径
    """

    chem_protein_links = chemical_protein.get_chem_protein_links(genes, protein_chemical_links_path, score, save)

    chem = chemical.get_chemicals(chem_protein_links, chemicals_path, save)

    tcm_chem_links = tcm_chemical.get_tcm_chem_links(chem, tcm_chemical_links_path, save)

    cm = tcm.get_tcm(tcm_chem_links, tcm_path, save)

    output.out_for_cyto(chem_protein_links, chem, genes, tcm_chem_links, cm)
