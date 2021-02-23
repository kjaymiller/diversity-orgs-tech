import React from "react";
import {
  buildAutocompleteQueryConfig,
  buildSearchOptionsFromConfig,
  buildSortOptionsFromConfig,
  getConfig,
} from "./config/config-helper";

import AppSearchAPIConnector from "@elastic/search-ui-app-search-connector";

import {
  ErrorBoundary,
  Facet,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Sorting,
  WithSearch
} from "@elastic/react-search-ui";

import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";


import SortingView from './SortingView';
import MultiCheckboxFacet from './FacetView';

const { hostIdentifier, searchKey, endpointBase, engineName } = getConfig();
const connector = new AppSearchAPIConnector({
  searchKey,
  engineName,
  hostIdentifier,
  endpointBase
});
const config = {
  searchQuery: {
    facets: {
        city: {
            type: "value",
            size: 30,
        },
        technology_focus: {
            type: "value",
            size: 30,
        },
        diversity_focus: {
            type: "value",
            size: 30,
        },
        parent_organization: {
            type: "value",
            size: 30,
        }
    },
    ...buildSearchOptionsFromConfig()
  },
  autocompleteQuery: buildAutocompleteQueryConfig(),
  apiConnector: connector,
  alwaysSearchOnInitialLoad: false
};


function ResultView(props) {
    const hasLink = <a href={props?.result?.url?.raw}>
          {props?.result?.name?.raw}
        </a>

    const noLink = props?.result?.name?.raw

    function parentOrg () { 
        if (props?.result?.parent_organization?.snippet) {
            return <small className="parentOrg mx-2"><a href={props.result?.global_org_url_from_parent_organization?.raw}>{props.result.parent_organization.raw}</a></small>
        }

        return ''
    }

    function smallDivs (field) {
        return field ? <small className="mx-2">{field}</small> : ''
    }

    function linkOption () {
        const links = []
        if (props?.result?.links?.raw){

            for (let link of props?.result?.links?.raw) {

                if (link.includes('twitter.com')) {
                   links.push(<a href={link}><img alt="twitter {props.result.name.raw}" src="https://kjaymiller.s3-us-west-2.amazonaws.com/images/Twitter_icon_square_logo.jpg" className="w-6 rounded shadow" /></a>)
                    }

                if (link.includes('meetup.com')) {
                    links.push(<a href={link}><img alt="meetup {props.result.name.raw}" src="https://kjaymiller.s3-us-west-2.amazonaws.com/images/meetup-logo-m-swarm-thumb.jpg" className="w-6" /></a>)
                }

                if (link.includes('facebook.com')) {
                    links.push(<a href={link}><img alt="facebook {props.result.name.raw}" src="https://kjaymiller.s3-us-west-2.amazonaws.com/images/1-facebook-colored-svg-copy-256.png" className="w-6" /></a>)
                }
            }

        }

        console.log(props?.result)
        return links
    }


    return <div className="lg:flex lg:jusitify-between items-center rounded-lg shadow-lg p-6">
            <div className="lg:w-1/4 w-1/4 lg:p-8">
                <img 
                    src={props?.result?.organization_logo?.raw}
                    alt={props?.result?.name?.raw} Logo
                />
            </div>
            <div className="">
                {props?.result?.diversity_focus?.raw.map((o) => smallDivs(o))}
                {parentOrg()}
                <h1 className="text-3xl my-3">{props?.result?.url?.raw ? hasLink : noLink}</h1>
            <div className="flex items-center">
                {smallDivs(props?.result?.city?.raw)}
                {linkOption()}
            </div>
            </div>
        </div>
} 


export default function Search() {
  return (
    <div className="container px-2 mx-auto my-4">
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                  header={<SearchBox autocompleteSuggestions={true} />}
                  sideContent={
                    <div>
                      {wasSearched && (
                        <Sorting
                          label={"Sort"}
                          sortOptions={buildSortOptionsFromConfig()}
                          view={SortingView}
                        />
                      )}
                      <Facet
                        field="city"
                        label="City"
                        filterType="any"
                        view={MultiCheckboxFacet}
                        isFilterable={true}
                      />
                      <Facet
                        field="parent_organization"
                        label="Parent Organization"
                        view={MultiCheckboxFacet}
                        isFilterable={false}
                      />
                      <Facet
                        field="diversity_focus"
                        label="Diversity Focus"
                        filterType="any"
                        view={MultiCheckboxFacet}
                      />
                      <Facet
                        field="technology_focus"
                        label="Technology Focus"
                        filterType="any"
                        view={MultiCheckboxFacet}
                        isFilterable={true}
                      />
                    </div>
                  }
                  bodyContent={
                    <Results
                      titleField={getConfig().titleField}
                      urlField={getConfig().urlField}
                      shouldTrackClickThrough={true}
                      resultView={ResultView}
                    />
                  }
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
    <footer>
        <p>
            Made by <a href="https://kjaymiller.com">kjaymiller</a>
        </p>
        <p><a href="./about.html"><strong>About</strong></a></p>
    </footer>
      </div>
  );
}

