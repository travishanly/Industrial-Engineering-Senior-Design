# Industrial-Engineering-Senior-Design

_The code in this repository, along with the text below, were submitted as part of a senior design project at Georgia Tech._

The Home Depot (THD) is the third largest container importer in North America. Its product suppliers operate roughly 1,000 factories in over 40 countries. THD’s International Logistics (IL) department manages trade operations, trade compliance, and trade risk for all of these imports and spends approximately \[REDACTED] annually for container shipping on the ocean carrier process. This process includes the scheduling and allocation of all purchase orders (POs) to the carriers that THD partners with. The department, however, lacks a dynamic method to determine the cheapest allocation while satisfying demands of the carriers, THD, and origin ports, which causes the department to exceed its annual targeted spend. 

Annual carrier contracts, carrier schedules, origin dwell times, and capacity constraints determine how POs are assigned to carriers. Currently, the allocation process is completed manually by two third-party logistics teams and an IL analyst. The objective of the allocation process is to achieve +/- 5% compliance variability with carrier allocation percentages based on annual contracts while reducing costs. The manual process does not minimize the target allocation percentage variability past the  +/- 5% compliance and consequently fails to reduce the overall spend.

The proposed solution is an optimization model that is used by an automated tool that produces an allocation of POs to carriers and shipping lanes. The tool determines the cheapest routes while meeting constraints based on priority. This dynamic system can be adjusted based on user preferences and is adaptable towards unexpected carrier changes. 

The model reduces spend and removes the necessity of the third party logistics companies from this process. The annualized cost savings is approximately $3.2M, and the allocation % error is decreased by 50%.
